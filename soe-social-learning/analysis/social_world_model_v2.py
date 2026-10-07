from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional, Tuple
import torch
import torch.nn as nn
import torch.nn.functional as F

@dataclass
class SocialWorldConfig:
    self_dim: int = 32
    pair_dim: int = 24
    context_dim: int = 24
    intervention_dim: int = 8
    neural_dim: int = 32
    hidden: int = 128
    relation_hidden: int = 128
    slow_hidden: int = 96
    n_actions: int = 32
    n_outcomes: int = 16
    n_social_contents: int = 24
    n_interventions: int = 16
    n_identity_slots: int = 256
    max_agents: int = 4
    future_steps: int = 8
    dropout: float = 0.1

class MLP(nn.Module):
    def __init__(self, din: int, dout: int, hidden: int, dropout: float):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(din, hidden), nn.SiLU(), nn.LayerNorm(hidden),
            nn.Dropout(dropout), nn.Linear(hidden, dout)
        )
    def forward(self, x):
        return self.net(x)

class DirectedRelationBlock(nn.Module):
    """Dense directed social graph for <=4 mice, without torch_geometric."""
    def __init__(self, h: int, pair_dim: int, dropout: float):
        super().__init__()
        self.edge = MLP(2*h + pair_dim, h, h, dropout)
        self.q = nn.Linear(h, h, bias=False)
        self.k = nn.Linear(h, h, bias=False)
        self.v = nn.Linear(h, h, bias=False)
        self.out = nn.Sequential(nn.Linear(2*h, h), nn.SiLU(), nn.LayerNorm(h))
    def forward(self, nodes, pair, agent_mask):
        # nodes: [B,T,N,H], pair: [B,T,N,N,P], mask: [B,T,N]
        B,T,N,H = nodes.shape
        src = nodes.unsqueeze(3).expand(B,T,N,N,H)
        dst = nodes.unsqueeze(2).expand(B,T,N,N,H)
        e = self.edge(torch.cat([src,dst,pair], dim=-1))
        score = (self.q(dst) * self.k(e)).sum(-1) / (H ** 0.5)
        valid = agent_mask.unsqueeze(2) & agent_mask.unsqueeze(3)
        eye = torch.eye(N, device=nodes.device, dtype=torch.bool).view(1,1,N,N)
        valid = valid & ~eye
        score = score.masked_fill(~valid, -1e4)
        attn = torch.softmax(score, dim=-1)
        attn = attn * valid.float()
        denom = attn.sum(-1, keepdim=True).clamp_min(1e-6)
        attn = attn / denom
        msg = (attn.unsqueeze(-1) * self.v(e)).sum(dim=3)
        return self.out(torch.cat([nodes,msg], dim=-1))

class HierarchicalMemory(nn.Module):
    """Separate fast interaction memory from slower relationship/homeostatic memory."""
    def __init__(self, h: int, slow: int):
        super().__init__()
        self.fast = nn.GRU(h, h, batch_first=True)
        self.relationship = nn.GRU(h, slow, batch_first=True)
        self.need = nn.GRU(h, slow, batch_first=True)
        self.credit = nn.GRU(h, slow, batch_first=True)
        self.mix = nn.Sequential(nn.Linear(h + 3*slow, h), nn.SiLU(), nn.LayerNorm(h))
    def forward(self, x):
        # x [B,T,H]
        fast,_ = self.fast(x)
        rel,_ = self.relationship(x)
        need,_ = self.need(x)
        credit,_ = self.credit(x)
        return self.mix(torch.cat([fast, rel, need, credit], dim=-1)), {
            "fast": fast, "relationship": rel, "social_need": need, "credit": credit
        }

class SocialWorldModelV2(nn.Module):
    """
    Mouse-first relational social world model.

    Input contract:
      self_state       [B,T,N,self_dim]
      pair_state       [B,T,N,N,pair_dim]
      agent_mask       [B,T,N] bool
      identity_id      [B,T,N] long, -1 for unknown
      context          [B,T,context_dim]
      intervention_id  [B,T] long, 0=no intervention
      neural_state     optional [B,T,neural_dim]
      focal_agent      optional [B,T] long; defaults to 0

    Outputs:
      next_action, next_target, next_outcome, next_content,
      future_latent, efficacy, social_need, value/credit,
      optional neural prediction and intervention counterfactual hooks.
    """
    def __init__(self, cfg: SocialWorldConfig):
        super().__init__()
        self.cfg = cfg
        h = cfg.hidden
        self.self_enc = MLP(cfg.self_dim, h, h, cfg.dropout)
        self.id_emb = nn.Embedding(cfg.n_identity_slots + 1, h)
        self.context_enc = MLP(cfg.context_dim, h, h, cfg.dropout)
        self.intervention_emb = nn.Embedding(cfg.n_interventions, cfg.intervention_dim)
        self.int_enc = MLP(cfg.intervention_dim, h, h, cfg.dropout)
        self.rel1 = DirectedRelationBlock(h, cfg.pair_dim, cfg.dropout)
        self.rel2 = DirectedRelationBlock(h, cfg.pair_dim, cfg.dropout)
        self.focal_mix = nn.Sequential(nn.Linear(4*h, h), nn.SiLU(), nn.LayerNorm(h))
        self.neural_fuse_norm = nn.LayerNorm(h)
        self.neural_gate = nn.Linear(2*h, h)
        nn.init.zeros_(self.neural_gate.weight)
        nn.init.constant_(self.neural_gate.bias, -2.0)
        self.memory = HierarchicalMemory(h, cfg.slow_hidden)
        self.neural_memory = nn.GRU(h, h, batch_first=True)

        self.action_head = nn.Linear(h, cfg.n_actions)
        self.multimodal_action_head = nn.Linear(h, cfg.n_actions)
        self.target_query = nn.Linear(h, h)
        self.target_key = nn.Linear(h, h)
        self.outcome_head = nn.Linear(h, cfg.n_outcomes)
        self.content_head = nn.Linear(h, cfg.n_social_contents)

        self.efficacy_head = nn.Linear(h, 1)
        self.value_head = nn.Linear(h, 1)
        self.need_head = nn.Linear(cfg.slow_hidden, 1)

        self.future_cell = nn.GRUCell(h, h)
        self.future_head = nn.Linear(h, h)

        self.neural_encoder = MLP(cfg.neural_dim, h, h, cfg.dropout)
        self.neural_pred = nn.Linear(h, cfg.neural_dim)

    def _identity(self, ids):
        ids = ids.clone()
        ids = torch.where(ids < 0, torch.full_like(ids, self.cfg.n_identity_slots), ids)
        ids = ids.clamp_max(self.cfg.n_identity_slots)
        return self.id_emb(ids)

    def encode_scene(self, batch: Dict[str, torch.Tensor]):
        x = self.self_enc(batch["self_state"]) + self._identity(batch["identity_id"])
        mask = batch["agent_mask"].bool()
        x = self.rel1(x, batch["pair_state"], mask)
        x = self.rel2(x, batch["pair_state"], mask)

        B,T,N,H = x.shape
        focal = batch.get("focal_agent")
        if focal is None:
            focal = torch.zeros(B,T, dtype=torch.long, device=x.device)
        gather_idx = focal[...,None,None].expand(B,T,1,H)
        focal_x = x.gather(2, gather_idx).squeeze(2)

        valid = mask.float().unsqueeze(-1)
        group = (x*valid).sum(2) / valid.sum(2).clamp_min(1.0)
        ctx = self.context_enc(batch["context"])
        intr = self.int_enc(self.intervention_emb(batch["intervention_id"]))
        base_scene = self.focal_mix(torch.cat([focal_x, group, ctx, intr], dim=-1))
        if "neural_state" in batch and batch["neural_state"] is not None:
            neural_ctx = self.neural_encoder(batch["neural_state"])
            # Stop-gradient on the core scene prevents a neural auxiliary loss from
            # degrading the validated social/behavioral representation in small datasets.
            core_for_neural = base_scene.detach()
            gate = torch.sigmoid(self.neural_gate(torch.cat([core_for_neural, neural_ctx], dim=-1)))
            multimodal_scene = self.neural_fuse_norm(core_for_neural + gate * neural_ctx)
        else:
            multimodal_scene = base_scene.detach()
        return base_scene, multimodal_scene, x, mask

    def forward(self, batch: Dict[str, torch.Tensor]):
        core_scene, multimodal_scene, nodes, mask = self.encode_scene(batch)
        z, memories = self.memory(core_scene)
        neural_z, _ = self.neural_memory(multimodal_scene)

        tq = self.target_query(z).unsqueeze(2)
        tk = self.target_key(nodes)
        target_logits = (tq * tk).sum(-1) / (z.shape[-1] ** 0.5)
        target_logits = target_logits.masked_fill(~mask, -1e4)

        out = {
            "latent": z,
            "behavior_latent": z,
            "multimodal_latent": neural_z,
            "next_action_logits": self.action_head(z),
            "next_action_logits_multimodal": self.multimodal_action_head(neural_z),
            "next_target_logits": target_logits,
            "next_outcome_logits": self.outcome_head(z),
            "next_content_logits": self.content_head(z),
            "social_efficacy": self.efficacy_head(z).squeeze(-1),
            "social_value_credit": self.value_head(z).squeeze(-1),
            "social_need": self.need_head(memories["social_need"]).squeeze(-1),
            "memory": memories
        }

        out["neural_prediction"] = self.neural_pred(neural_z)
        if "neural_state" in batch and batch["neural_state"] is not None:
            out["neural_alignment_latent"] = self.neural_encoder(batch["neural_state"])
        return out

    def rollout_latent(self, z0: torch.Tensor, steps: Optional[int]=None):
        steps = steps or self.cfg.future_steps
        h = z0
        preds = []
        inp = z0
        for _ in range(steps):
            h = self.future_cell(inp, h)
            inp = self.future_head(h)
            preds.append(inp)
        return torch.stack(preds, dim=-2)

    @torch.no_grad()
    def intervention_replay(self, batch: Dict[str, torch.Tensor], intervention_a: int, intervention_b: int):
        a = {k:v for k,v in batch.items()}
        b = {k:v for k,v in batch.items()}
        a["intervention_id"] = torch.full_like(batch["intervention_id"], intervention_a)
        b["intervention_id"] = torch.full_like(batch["intervention_id"], intervention_b)
        oa, ob = self(a), self(b)
        return {
            "delta_action_logits": oa["next_action_logits"] - ob["next_action_logits"],
            "delta_efficacy": oa["social_efficacy"] - ob["social_efficacy"],
            "delta_value_credit": oa["social_value_credit"] - ob["social_value_credit"],
            "delta_latent": oa["latent"] - ob["latent"]
        }

def multitask_loss(out: Dict[str, torch.Tensor], target: Dict[str, torch.Tensor],
                   weights: Optional[Dict[str,float]]=None) -> Tuple[torch.Tensor, Dict[str,float]]:
    w = {
        "action":1.0, "target":0.5, "outcome":0.8, "content":0.8,
        "future":1.0, "efficacy":0.5, "neural":0.25, "need":0.25
    }
    if weights: w.update(weights)
    losses = {}
    if "action" in target:
        losses["action"] = F.cross_entropy(out["next_action_logits"].flatten(0,1), target["action"].flatten())
    if "target_agent" in target:
        losses["target"] = F.cross_entropy(out["next_target_logits"].flatten(0,1), target["target_agent"].flatten())
    if "outcome" in target:
        losses["outcome"] = F.cross_entropy(out["next_outcome_logits"].flatten(0,1), target["outcome"].flatten())
    if "social_content" in target:
        losses["content"] = F.cross_entropy(out["next_content_logits"].flatten(0,1), target["social_content"].flatten())
    if "future_latent" in target:
        pred = out["latent"]
        losses["future"] = 1 - F.cosine_similarity(pred, target["future_latent"], dim=-1).mean()
    if "efficacy" in target:
        losses["efficacy"] = F.mse_loss(out["social_efficacy"], target["efficacy"])
    if "social_need" in target:
        losses["need"] = F.mse_loss(out["social_need"], target["social_need"])
    if "neural_state" in target and "neural_prediction" in out:
        losses["neural"] = F.mse_loss(out["neural_prediction"], target["neural_state"])
    total = sum(w[k]*v for k,v in losses.items())
    return total, {k:float(v.detach()) for k,v in losses.items()}

if __name__ == "__main__":
    cfg = SocialWorldConfig()
    model = SocialWorldModelV2(cfg)
    print("parameters", sum(p.numel() for p in model.parameters()))
