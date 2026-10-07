from pathlib import Path
import csv, json

ROOT = Path(r"H:\brain_world_model_20261005\push_stage23_clean\soe-social-learning")
DATA = ROOT / "data"
DOCS = ROOT / "docs"
DATA.mkdir(parents=True, exist_ok=True)
DOCS.mkdir(parents=True, exist_ok=True)

datasets = [
{"dataset":"User SOE / social-observation feeding","year":"2026","species":"mouse","agents":"dyad","modalities":"pose; event ethogram; feeding/lick; VTA DA photometry; perturbation; OXT cohorts","scale":"27+ held-out animals across multiple cohorts","social_axes":"observation; demonstrator feeding content; self feeding; active/passive/unrewarded outcome; familiarity; visual access","access":"local authority","url":"","priority":"P0","integration_role":"core causal and mechanistic grounding","status":"INGESTED"},
{"dataset":"MABe Challenge 2025","year":"2025","species":"mouse","agents":"1-4 mice","modalities":"multi-animal pose; metadata; frame/event behavior labels","scale":"400+ h; 20+ recording systems/labs; >30 social/non-social behaviors; 2.84 GB competition package","social_axes":"agent-target action; attack; chase; sniff/investigation; grooming; mounting; group context; identity metadata","access":"Kaggle; CC BY 4.0","url":"https://www.kaggle.com/competitions/MABe-mouse-behavior-detection","priority":"P0","integration_role":"largest heterogeneous mouse-social pretraining and cross-lab generalization benchmark","status":"REGISTERED_FETCH_PENDING"},
{"dataset":"CalMS21","year":"2021","species":"mouse","agents":"dyad","modalities":"7-keypoint pose; video subset; frame behavior labels","scale":"6M unlabeled pose frames; >1M labeled pose frames","social_axes":"attack; mount; close investigation; sniff-face; approach; disengage; grooming; annotation-style transfer","access":"CaltechDATA; CC BY-NC-SA","url":"https://data.caltech.edu/records/s0vdx-0k302","priority":"P0","integration_role":"dyadic social representation pretraining; few-shot behavior; annotator-domain robustness","status":"INGESTED_TASK1_89SEQ_HELD_ANIMAL_RELATION_VALIDATED"},
{"dataset":"MABe22 mouse triplets","year":"2022/2023","species":"mouse","agents":"triplet","modalities":"pose; video subset; downstream condition labels","scale":"4.7M video+pose frames; 10M pose-only frames; mouse trajectory arrays publicly released","social_axes":"group interaction; strain; time-of-day; optogenetic condition; multi-agent representation","access":"CaltechDATA","url":"https://data.caltech.edu/records/8kdn3-95j37","priority":"P0","integration_role":"three-mouse group-state pretraining and representation-learning benchmark","status":"INGESTED_784SEQ_GROUP_PRETRAINING"},
{"dataset":"CRIM13","year":"2012","species":"mouse","agents":"dyad","modalities":"video; social behavior annotations","scale":"resident-intruder benchmark; 13 action categories","social_axes":"investigation; aggression; mounting; social action recognition","access":"public benchmark; also bundled in MABe 2025 training","url":"https://www.kaggle.com/competitions/MABe-mouse-behavior-detection","priority":"P1","integration_role":"cross-domain behavior recognition stress test","status":"VIA_MABE2025"},
{"dataset":"13-region social behavior network multifiber photometry","year":"2023","species":"mouse","agents":"dyad","modalities":"13-region Esr1+ multifiber Ca2+ photometry; behavior annotations","scale":"5 hypothalamic + 5 amygdala + 3 other social-network regions","social_axes":"male-male aggression/defense; male-female mating; network state","access":"Zenodo open","url":"https://zenodo.org/records/8128564","priority":"P0","integration_role":"brain-wide social-state latent alignment and region-to-region dynamics","status":"INGESTED_8_ANIMALS_ARCHITECTURE_GATE"},
{"dataset":"VTA DA social interaction / social prediction error","year":"2022","species":"mouse","agents":"dyad","modalities":"VTA dopamine single-unit spiking; event timing; instrumental social task","scale":"released data supporting social interaction and social reinforcement-learning figures","social_axes":"social interaction; social reward; social prediction error; instrumental learning","access":"Zenodo open","url":"https://doi.org/10.5281/zenodo.5564893","priority":"P0","integration_role":"independent neural validation of social value and prediction-error heads","status":"REGISTERED_FETCH_PENDING"},
{"dataset":"NAc-core dopamine during social behaviors","year":"2024/2025","species":"mouse","agents":"dyad","modalities":"GRABDA2m photometry; behavior; optogenetics; histology","scale":"male and female mouse social behaviors","social_axes":"social reward; approach; interaction stages; DA dynamics","access":"NYU Data Catalog; approval required","url":"https://datacatalog.med.nyu.edu/dataset/10686","priority":"P1","integration_role":"independent reward-system target once access obtained","status":"ACCESS_REQUEST_REQUIRED"},
{"dataset":"Mouse USV social interaction audio-video","year":"2026","species":"mouse","agents":"social interaction","modalities":"ultrasonic audio; video clips; behavior annotations","scale":"OSF dataset accompanying 2026 behavior-from-USV model","social_axes":"vocal communication; interaction state; multimodal social behavior","access":"OSF open","url":"https://osf.io/rvkb9","priority":"P1","integration_role":"audio/social-communication encoder and cross-modal future prediction","status":"REGISTERED_FETCH_PENDING"},
{"dataset":"Social isolation BLA-mPFC calcium imaging","year":"2026","species":"mouse","agents":"social-history context","modalities":"in vivo calcium imaging; behavior; social rank/isolation metadata","scale":"104.7 GB; 359 files","social_axes":"social isolation; rank; affective state; BLA-mPFC circuit","access":"DANDI 001454; CC BY 4.0","url":"https://dandiarchive.org/dandiset/001454","priority":"P1","integration_role":"social-homeostasis/context state and affective circuit transfer","status":"REGISTERED_FETCH_PENDING"},
{"dataset":"CA2 social-memory / Shank3 dataset","year":"2026","species":"mouse","agents":"social recognition","modalities":"behavior; electrophysiology; tracking; histology","scale":"91.5 GB Dryad release","social_axes":"social memory; novelty/familiarity; CA2 physiology; autism model","access":"Dryad open","url":"https://datadryad.org/dataset/doi:10.5061/dryad.wm37pvn2t","priority":"P1","integration_role":"familiarity/identity memory head and disease-generalization benchmark","status":"REGISTERED_FETCH_PENDING"},
{"dataset":"STFP cortical-amygdala social memory","year":"2024","species":"mouse","agents":"demonstrator-observer","modalities":"behavior; circuit perturbation; molecular/source data","scale":"Nature STFP consolidation study","social_axes":"socially transmitted food preference; olfactory identity/content; consolidation","access":"paper source data / supplement","url":"https://www.nature.com/articles/s41586-024-07632-5","priority":"P0","integration_role":"closest external paradigm to SOE; social information -> food choice -> long-term memory","status":"SOURCE_DATA_AUDIT_PENDING"}
]

datasets += [
{"dataset":"MARS social behavior benchmark / BENTO","year":"2021","species":"mouse","agents":"dyad","modalities":"top/front video; pose; behavior annotations; multimodal neuroscience visualization","scale":"14.2 h annotated social behavior corpus plus pose/annotation benchmark resources","social_axes":"resident-intruder interaction; investigation; attack; mount; annotation reliability","access":"CaltechDATA / public code","url":"https://elifesciences.org/articles/63720","priority":"P1","integration_role":"human-level dyadic social-action benchmark and annotation-reliability baseline","status":"REGISTERED"},
{"dataset":"maDLC multi-animal mouse benchmarks","year":"2022","species":"mouse","agents":"dyad/triplet","modalities":"video; identity-aware multi-animal keypoints","scale":"released multi-animal benchmark datasets including tri-mouse and parenting","social_axes":"persistent identity under occlusion; group tracking; parenting/social proximity","access":"DeepLabCut benchmark / Zenodo","url":"https://www.nature.com/articles/s41592-022-01443-0","priority":"P2","integration_role":"identity-tracking stress test before relation-state modeling","status":"REGISTERED"},
{"dataset":"SLEAP multi-animal benchmarks","year":"2022","species":"mouse + other","agents":"multi-animal","modalities":"video; pose; identity tracks; real-time closed-loop","scale":"seven multi-animal datasets across species including mice","social_axes":"identity tracking; interaction-triggered closed-loop control","access":"SLEAP public datasets","url":"https://www.nature.com/articles/s41592-022-01426-1","priority":"P2","integration_role":"pose/identity front-end and real-time social closed-loop benchmark","status":"REGISTERED"}
]

models = [
{"family":"MABe2025 GNN + Egocentric Squeezeformer","year":"2025","type":"supervised multi-agent sequence","core_idea":"TransformerConv social graph -> per-mouse egocentric Squeezeformer -> pairwise relation head; invariant self/pair features","strength":"top-5 cross-lab mouse social-action system; explicitly models mouse-to-mouse graph and egocentric invariance","weakness":"classifier, not generative world model; heavy ensemble","swm_use":"adopt relational graph encoder, egocentric canonicalization, missing-keypoint robustness","source":"https://www.kaggle.com/competitions/MABe-mouse-behavior-detection/writeups/5th-place-gnn-egocentric-squeezeformer"},
{"family":"MABe2025 XGB + NN ensemble","year":"2025","type":"supervised multi-agent sequence","core_idea":"rich kinematic and pair features; multi-dilation conv/residual NN; per-lab specialization; metadata","strength":"strong practical robustness across heterogeneous labs and rare behaviors","weakness":"lab-specific selection/calibration limits unified representation","swm_use":"borrow pair features, arena/context metadata and heterogeneous-lab normalization as controls","source":"https://www.kaggle.com/competitions/MABe-mouse-behavior-detection/writeups/4th-place-solution-xgb-nn-ensemble"},
{"family":"MABe2025 LSTM + XGBoost","year":"2025","type":"supervised sequence + boosted trees","core_idea":"512-frame temporal windows plus engineered relational kinematics; blend NN and trees","strength":"high-performing simple temporal baseline","weakness":"not latent-dynamics or causal","swm_use":"strong classical comparator and feature audit","source":"https://www.kaggle.com/competitions/MABe-mouse-behavior-detection/writeups/3rd-place-solution"},
{"family":"MABe2025 ST-GCN + Transformer","year":"2025","type":"spatiotemporal graph sequence","core_idea":"jointly model agent-target pairs with skeleton graph and temporal transformer","strength":"direct skeleton topology + social pair modeling","weakness":"supervised action segmentation","swm_use":"architecture comparator for body graph versus learned relation graph","source":"https://www.kaggle.com/competitions/MABe-mouse-behavior-detection/writeups/10th-place-solution-st-gcn-transformer"},
{"family":"CS-IGANet","year":"2025","type":"cross-skeleton graph transformer","core_idea":"intra-, inter- and cross-skeleton node interaction plus interaction-aware attention and SSL auxiliary objective","strength":"explicit multilevel interaction representation","weakness":"behavior recognition benchmark rather than generative dynamics","swm_use":"candidate pair-graph block; benchmark against simpler TransformerConv","source":"https://pubmed.ncbi.nlm.nih.gov/40030903/"},
{"family":"SBeA","year":"2024","type":"3D multi-animal pose/identity/unsupervised behavior","core_idea":"few-shot 3D pose; label-free identity; unsupervised dynamic behavior embedding","strength":"identity-preserving multi-animal 3D social phenotype discovery","weakness":"primarily behavior atlas, not neural/world prediction","swm_use":"identity tracking and unsupervised social motif pretraining","source":"https://www.nature.com/articles/s42256-023-00776-5"},
{"family":"TREBA / Task Programming","year":"2021","type":"self-supervised trajectory representation","core_idea":"programmatic expert tasks such as facing angle, speeds, nose-nose/nose-tail distances, head-body angle; contrastive/consistency objectives","strength":"encodes ethological priors and cuts annotation needs up to 10x in mouse tasks","weakness":"fixed short trajectory embedding; no causal/world rollout","swm_use":"turn expert social geometry into auxiliary pretraining objectives rather than hand-coded final features","source":"https://pmc.ncbi.nlm.nih.gov/articles/PMC9766046/"},
{"family":"MABe22 representation benchmark","year":"2023","type":"self-supervised multi-agent representation","core_idea":"benchmark latent representations on triplet mice and multiple downstream experimental variables","strength":"tests whether learned representations preserve biologically relevant social/context variables","weakness":"benchmark, not one canonical architecture","swm_use":"external representation contract for group state","source":"https://proceedings.mlr.press/v202/sun23g/sun23g.pdf"},
{"family":"Keypoint-MoSeq","year":"2024","type":"generative unsupervised pose dynamics","core_idea":"AR-HMM-like discrete behavioral syllables linked to continuous keypoint dynamics","strength":"strong unsupervised segmentation of pose dynamics with interpretable motifs","weakness":"single-agent orientation unless extended; not relational world model by default","swm_use":"motif tokenizer / discrete behavior codebook comparator","source":"https://www.nature.com/articles/s41592-024-02318-2"},
{"family":"VAME","year":"2022+","type":"variational recurrent behavioral embedding","core_idea":"RNN variational autoencoder over pose/time series followed by clustering","strength":"unsupervised temporal latent; scalable behavioral segmentation","weakness":"does not explicitly encode agent-target graph or causal interventions","swm_use":"unsupervised temporal latent baseline","source":"https://ethoml.github.io/VAME/docs/intro/"},
{"family":"DeepEthogram","year":"2021","type":"raw-video supervised behavior classifier","core_idea":"motion + image feature CNN -> frame ethogram","strength":"pixel-level behavior signal and rare behavior performance","weakness":"no explicit relational latent/world state","swm_use":"optional video encoder teacher for pose-world pretraining","source":"https://elifesciences.org/articles/63377"},
{"family":"CEBRA","year":"2023","type":"contrastive joint neural-behavior representation","core_idea":"behavior- or self-supervised contrastive embedding of neural and behavioral time series","strength":"consistent nonlinear latent across sessions/modalities; natural neural-behavior alignment","weakness":"embedding objective alone does not generate future trajectories","swm_use":"neural-social latent alignment loss and cross-session consistency metric","source":"https://www.nature.com/articles/s41586-023-06031-6"},
{"family":"Multifiber social-network state-space model","year":"2024","type":"dynamic latent variable / state-space","core_idea":"latent-state analysis linking simultaneous 13-region social-network photometry to annotated aggression/mating behavior","strength":"brain-wide social-network dynamics rather than one-region readout","weakness":"population-average photometry and limited subjects/tasks","swm_use":"neural latent-dynamics benchmark and regional state decoder","source":"https://pmc.ncbi.nlm.nih.gov/articles/PMC11246699/"},
{"family":"Current SLM / SWM","year":"2026","type":"mechanistic + recurrent generative social world model","core_idea":"multiscale state, Observe policy, source/outcome credit, social efficacy, event/motif future rollout, neural and perturbation grounding","strength":"directly tied to causal SOE, Visual Block, VTA DA, JAWS; cross-animal and cross-species tests","weakness":"current agent ontology is narrow; mostly dyadic observer-demonstrator feeding","swm_use":"core model to expand rather than replace","source":"local authority"}
]

models += [
{"family":"MARS / BENTO","year":"2021","type":"supervised dyadic social action + multimodal viewer","core_idea":"top/front pose estimation -> engineered social features -> behavior classifier; BENTO aligns behavior with neural data","strength":"human-level mouse social behavior classification; explicit annotator reliability and multimodal neuroscience workflow","weakness":"predefined labels; not a generative world state","swm_use":"strong dyadic classifier baseline, annotation ceiling and neural/behavior alignment interface","source":"https://elifesciences.org/articles/63720"},
{"family":"LISBET","year":"2023/2024","type":"self-supervised social behavior transformer","core_idea":"Transformer representation from body tracking with supervised classification, unsupervised motif segmentation and phenotyping","strength":"mouse-specific social motif discovery; VTA electrophysiology signatures reported for learned motifs","weakness":"segmentation/embedding rather than explicit future/counterfactual world dynamics","swm_use":"Transformer motif encoder and independent VTA-aligned representation comparator","source":"https://arxiv.org/abs/2311.04069"},
{"family":"A-SOiD","year":"2024","type":"active-learning + unsupervised behavior discovery","core_idea":"iterative expert-guided active learning plus unsupervised subdivision of ambiguous interaction space","strength":"reported 85% less training data in socially interacting mice with competitive classification and interpretable sub-actions","weakness":"behavior segmentation rather than relational future model","swm_use":"active-learning annotation loop and interpretable sub-action discovery for rare social events","source":"https://www.nature.com/articles/s41592-024-02200-1"},
{"family":"B-SOiD","year":"2021","type":"unsupervised pose behavior clustering + fast classifier","core_idea":"spatiotemporal pose statistics -> unsupervised clusters -> fast supervised prediction","strength":"subject/lab generalization and high temporal resolution","weakness":"primarily single-agent/sub-action segmentation; social relations need explicit extension","swm_use":"unsupervised motif baseline and cross-lab segmentation control","source":"https://www.nature.com/articles/s41467-021-25420-x"},
{"family":"DeepOF","year":"2022+","type":"multi-mouse supervised + unsupervised behavior toolkit","core_idea":"DLC/Social-LEAP tracking -> relational features -> supervised social behavior plus VADE/VQVAE/contrastive unsupervised models","strength":"supports arbitrary mouse number, long recordings and interactive-behavior contrastive representation","weakness":"analysis toolkit rather than one causal/generative model","swm_use":"feature/behavior extraction baseline and contrastive social-representation comparator","source":"https://deepof.ai/"},
{"family":"SimBA","year":"2021+","type":"explainable supervised behavior classification toolkit","core_idea":"pose from many trackers -> engineered features -> user-trained classifiers for social/non-social behavior","strength":"broad practical adoption and interpretable classifier workflow","weakness":"depends on predefined annotated behavior; no learned world dynamics","swm_use":"strong supervised feature-engineering baseline and QC pipeline","source":"https://github.com/sgoldenlab/simba"},
{"family":"SLEAP","year":"2022+","type":"multi-animal pose + identity tracking","core_idea":"top-down/bottom-up neural pose estimation, grouping and identity tracking; supports real-time social closed-loop control","strength":"accurate, data-efficient and fast multi-animal tracking; explicit identity continuity","weakness":"pose/identity infrastructure, not social-state learning","swm_use":"front-end identity-preserving keypoints and real-time intervention trigger infrastructure","source":"https://www.nature.com/articles/s41592-022-01426-1"},
{"family":"multi-animal DeepLabCut","year":"2022+","type":"multi-animal pose/assembly/tracking","core_idea":"keypoint estimation + animal assembly + local tracking + global tracklet stitching with optional identity prediction","strength":"strong occlusion/identity tracking and released mouse benchmarks","weakness":"tracking rather than behavior/world modeling","swm_use":"alternative pose/identity front-end and identity-swap audit","source":"https://www.nature.com/articles/s41592-022-01443-0"},
{"family":"AlphaTracker","year":"2023","type":"multi-animal pose + identity + unsupervised clustering","core_idea":"top-down markerless tracking of similar unmarked animals followed by behavioral motif clustering","strength":"designed for social/group dynamics and challenging mouse hardware/occlusion conditions","weakness":"motif clustering not future/counterfactual dynamics","swm_use":"identity continuity and unsupervised social-motif comparator","source":"https://pmc.ncbi.nlm.nih.gov/articles/PMC10266280/"},
{"family":"Relational Social World Model v2","year":"2026","type":"entity + directed-relation graph + hierarchical fast/slow recurrent world model","core_idea":"persistent mouse entities, directed agent-target edges, fast interaction dynamics, separate relationship/social-need/credit memories, multimodal neural context and intervention-conditioned rollout","strength":"designed to unify broad mouse-social pretraining with the validated SOE efficacy/credit/neural/causal framework","weakness":"architecture candidate until external-pretrain->held-SOE Stage30 transfer gates pass","swm_use":"next-generation core architecture; must beat identical scratch model and preserve social-content specificity","source":"local architecture candidate"}
]

priors = [
{"domain":"identity / familiarity","system":"dorsal CA2","finding":"Novel conspecifics occupy a low-dimensional geometry that supports abstraction; familiar littermates expand into higher-dimensional representations, while familiarity itself can be encoded abstractly across identity.","model_constraint":"Separate partner identity memory from familiarity state; allow familiarity-dependent representational dimensionality/capacity.","source":"https://www.sciencedirect.com/science/article/pii/S0896627324000473"},
{"domain":"identity / familiarity","system":"IL->NAcSh prefrontal projection","finding":"Projection neurons carry familiar-conspecific information across days and participate in social recognition.","model_constraint":"Long-timescale relationship memory should survive across sessions/days and influence value/approach.","source":"https://www.nature.com/articles/s41467-025-64264-7"},
{"domain":"identity / familiarity","system":"mPFC-Re circuit","finding":"mPFC and nucleus reuniens populations represent social stimuli; mPFC coding is stronger and Re perturbation degrades social recognition coding.","model_constraint":"Identity should be a distributed latent with circuit-specific readout, not a single metadata label.","source":"https://www.nature.com/articles/s41467-024-45376-y"},
{"domain":"identity / familiarity","system":"olfactory cortex + oxytocin","finding":"Oxytocin-dependent plasticity separates cortical representations of familiar mice and increases salience of familiar social odor representations.","model_constraint":"Sensory social identity encoder should be plastic and neuromodulator-gated; familiarity can increase rather than merely habituate representation.","source":"https://www.nature.com/articles/s41467-024-50113-6"},
{"domain":"social information memory","system":"COApm cortical amygdala","finding":"COApm integrates social and olfactory input and is specifically required for consolidation of socially transmitted food preference.","model_constraint":"Distinguish acquisition, consolidation, storage and retrieval; add delayed memory-consolidation objective for social food information.","source":"https://www.nature.com/articles/s41586-024-07632-5"},
{"domain":"social prediction error / value","system":"VTA dopamine","finding":"VTA DA activity encodes social interaction and social prediction error and supports social reinforcement learning.","model_constraint":"Include social reward/prediction-error head but test it against policy/credit alternatives and timing.","source":"https://www.nature.com/articles/s41593-021-00972-9"},
{"domain":"social motivation","system":"PVN oxytocin -> VTA / VTA outputs","finding":"Oxytocin and dopamine interact in social motivation; isolation can increase social craving and VTA-linked social interaction.","model_constraint":"Add slow social-need/homeostatic state that gates value and sampling policy.","source":"https://pmc.ncbi.nlm.nih.gov/articles/PMC11912778/"},
{"domain":"social homeostasis","system":"hypothalamic preoptic nucleus","finding":"Distinct populations encode social need and social satiety; rebound scales with isolation duration; touch is a key signal of social context.","model_constraint":"Explicit need/satiety latent with accumulation and consummatory reset; tactile contact must be a distinct observation channel.","source":"https://www.nature.com/articles/s41586-025-08617-8"},
{"domain":"opponent model / rank","system":"cMPOA Esr1 -> VMHvl","finding":"Neural activity reflects opponent fighting capability learned from traits/experience and suppresses aggression toward superior opponents.","model_constraint":"Represent partner capability/rank as a learned relational belief, not fixed identity metadata.","source":"https://www.nature.com/articles/s41593-023-01297-5"},
{"domain":"motivation vs action","system":"VMHvl shell and MPO->VMHvl inhibition","finding":"Distinct inhibitory mechanisms gate aggressive motivation versus attack action/endpoints.","model_constraint":"Separate latent drive/motivation from emitted action; action decoder should not be the world state itself.","source":"https://www.nature.com/articles/s41593-023-01563-6"},
{"domain":"experience-dependent social category","system":"VMHvl Esr1","finding":"Male/female social ensembles separate with social/sexual experience rather than being fully hardwired.","model_constraint":"Social category representation must be learnable and experience-dependent.","source":"https://www.nature.com/articles/nature23885"},
{"domain":"social-network transformations","system":"MeA -> BNSTpr -> MPOA/VMHvl","finding":"Social cue representations are transformed across an extended amygdala-hypothalamic network to organize appetitive-to-consummatory transitions.","model_constraint":"Use hierarchical relational state transitions, not a flat behavior label space.","source":"https://www.nature.com/articles/s41586-022-05057-6"},
{"domain":"persistent social/reproductive state","system":"female VMHvl","finding":"Low-dimensional line-attractor-like dynamics track mating state across tens of seconds.","model_constraint":"Include continuous persistent latent dynamics in addition to discrete motifs/events.","source":"https://www.nature.com/articles/s41586-024-07916-w"},
{"domain":"social sensory specialization","system":"medial amygdala lineages","finding":"MeA Foxp2 cells specialize for male cues/aggression whereas Dbx1-lineage cells respond broadly and strongly during ejaculation.","model_constraint":"Factor sensory identity/content channels from action state and allow cell-type-specific readouts.","source":"https://www.nature.com/articles/s41593-023-01475-5"},
{"domain":"communication","system":"ultrasonic vocalization","finding":"USVs carry information sufficient for automated prediction of social behavior in paired mice.","model_constraint":"Add synchronized audio token stream and cross-modal prediction between vocalization and pose/action.","source":"https://www.nature.com/articles/s41598-026-59401-1"},
{"domain":"social conflict / sex","system":"PVN oxytocin -> VTA","finding":"PVN oxytocin circuits regulate dyadic/intragroup aggression and dominance in a sex-dependent manner in wild mice.","model_constraint":"Sex and group context should gate intervention effects; include group-level state/personality/rank variables.","source":"https://www.nature.com/articles/s41593-024-01685-5"}
]

ontology = [
{"state":"self_kinematics","timescale":"10 ms-2 s","examples":"speed; acceleration; body shape; head direction; posture","observability":"pose/video","role":"instantaneous embodied state"},
{"state":"partner_kinematics","timescale":"10 ms-2 s","examples":"partner speed; heading; posture; movement","observability":"pose/video","role":"other-agent state"},
{"state":"dyadic_geometry","timescale":"10 ms-10 s","examples":"distance; bearing; facing; nose-nose/nose-tail; approach velocity; contact","observability":"pose/video","role":"relation edge"},
{"state":"agent_target_action","timescale":"0.1-10 s","examples":"approach; investigate; sniff; chase; attack; mount; groom; avoid; observe; feed","observability":"ethogram/latent motifs","role":"directed social action"},
{"state":"social_content","timescale":"0.1-30 s","examples":"partner feeding; reward availability; partner action/outcome; vocalization; threat cue","observability":"task/video/audio","role":"information acquired from other"},
{"state":"identity","timescale":"session-days","examples":"individual partner ID; sex; strain; role","observability":"metadata + sensory latent","role":"entity memory key"},
{"state":"familiarity_relationship","timescale":"minutes-days","examples":"novel/familiar; interaction history; trust/reliability; affiliation","observability":"latent + metadata","role":"long-term relational memory"},
{"state":"rank_capability","timescale":"minutes-days","examples":"dominance; opponent fighting ability; winner/loser history","observability":"interaction history","role":"partner belief / strategic state"},
{"state":"social_need_satiety","timescale":"minutes-days","examples":"isolation duration; reunion rebound; contact satisfaction","observability":"history/context","role":"homeostatic motivational latent"},
{"state":"social_policy","timescale":"trials-minutes","examples":"P(observe); P(approach); P(engage); action policy","observability":"model latent","role":"pre-action decision"},
{"state":"social_efficacy","timescale":"trials-minutes","examples":"expected usefulness of social information; demonstrator reliability","observability":"model latent","role":"prospective information value"},
{"state":"credit_value","timescale":"trials-days","examples":"source/outcome-specific credit; Q/value; reward expectancy","observability":"model latent + neural","role":"learning state"},
{"state":"prediction_error","timescale":"100 ms-seconds","examples":"APE; social RPE; outcome PE","observability":"derived model signal + neural","role":"learning update"},
{"state":"motivation_drive","timescale":"seconds-minutes","examples":"aggressive motivation; mating drive; feeding motivation","observability":"latent/neural","role":"separate desire from emitted action"},
{"state":"neural_social_state","timescale":"10 ms-minutes","examples":"VTA DA; 13-region SBN; CA2 identity geometry; VMHvl state","observability":"spikes/Ca/photometry","role":"biological grounding"},
{"state":"intervention","timescale":"experiment-defined","examples":"JAWS ON/OFF; optogenetic pattern; chemo; visual block","observability":"experimental token","role":"causal action on the world"},
{"state":"context","timescale":"session-days","examples":"arena; lab; device; time of day; hunger; social isolation; sex; genotype","observability":"metadata","role":"domain/context conditioning"},
{"state":"communication","timescale":"10 ms-seconds","examples":"USV; olfactory cue; tactile contact","observability":"audio/sensory/context","role":"social message channel"},
{"state":"group_state","timescale":"seconds-hours","examples":"triplet/group topology; subgroup; conflict; dominance hierarchy","observability":"multi-agent graph","role":"beyond-dyad social world"}
]

def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

write_csv(DATA/"SOCIAL_WORLD_DATASET_REGISTRY_v1.csv", datasets)
write_csv(DATA/"SOCIAL_WORLD_MODEL_ZOO_v1.csv", models)
write_csv(DATA/"SOCIAL_WORLD_BIOLOGICAL_PRIORS_v1.csv", priors)
write_csv(DATA/"SOCIAL_WORLD_STATE_ONTOLOGY_v1.csv", ontology)

atlas = {
    "generated_at":"2026-10-06",
    "status":"FIELD_SCALE_SOCIAL_WORLD_MODEL_V1",
    "mission":"Build a mouse-first relational social world model that represents agents, relations, social information, internal motivation, learning, long-term relationship memory, neural state and interventions, then predicts future behavior/neural dynamics and counterfactual outcomes.",
    "dataset_count":len(datasets),
    "model_family_count":len(models),
    "biological_prior_count":len(priors),
    "ontology_state_count":len(ontology),
    "priority_datasets":[d["dataset"] for d in datasets if d["priority"]=="P0"],
    "design_principles":[
      "Entity-centric: each mouse is a persistent entity with identity and memory.",
      "Relation-centric: directed agent->target edges carry geometry, interaction, reliability, rank and familiarity.",
      "Multi-timescale: frame kinematics, event memory, minutes-scale state and cross-day relationship memory are distinct.",
      "World-state not classifier: latent must support multi-step rollout, content counterfactuals and intervention conditioning.",
      "Biological grounding: neural recordings and causal perturbations constrain latent coordinates but do not define them.",
      "Mouse-first pretraining: exploit MABe2025/CalMS21/MABe22 before cross-species transfer.",
      "Strict generalization: held-animal, held-lab, held-partner, held-context and intervention-aware evaluation."
    ]
}
(DATA/"SOCIAL_WORLD_FIELD_ATLAS_v1.json").write_text(json.dumps(atlas, indent=2, ensure_ascii=False), encoding="utf-8")

md = f"""# Mouse Social World Model — field-scale blueprint v1
Date: 2026-10-06

## Mission
The target is not a better SOE classifier. The target is a **mouse-first social world model** that learns a reusable internal state of the social world from multiple animals, multiple timescales, neural recordings and interventions.

The state must answer four classes of questions:
1. **What is happening now?** Who is present, where are they, what are they doing, what information is available?
2. **What does each animal believe/value/need?** Familiarity, partner reliability, social need, reward/social credit, rank/capability and motivational state.
3. **What happens next?** Future social action, partner response, outcome, neural trajectory and longer multi-step interaction.
4. **What if the world changes?** Visual block, JAWS/optogenetic manipulation, changed partner, changed social content or altered social history.

## Why the current SOE/SWM is the right seed
The existing model already contains the rare ingredients missing from most behavior classifiers: content-specific observation, multiscale memory, prospective social efficacy, source/outcome credit, generative event/motif rollout, VTA temporal grounding and causal perturbations. The upgrade should therefore preserve the current SLM/SWM semantics while replacing the narrow observer-demonstrator state with a general multi-agent relational state.

## Architecture: Social World Model v2
### 1. Mouse/entity encoder
Each mouse receives a persistent entity token. Inputs include pose/kinematics, body configuration, sex/strain/age/device metadata when available, and an identity embedding that can be replaced by sensory identity when a literal ID is unavailable.

Use egocentric, scale-normalized features so the same action is represented similarly across arenas and labs. Preserve missing-keypoint masks rather than silently imputing everything.

### 2. Directed relation graph
At every time step create directed edges i->j with relative distance, bearing, facing, approach velocity, nose-to-nose/nose-to-tail distances, contact, target-relative body pose and recent interaction history.

A graph-attention/TransformerConv block updates each mouse from all other mice. This directly imports the strongest lesson from MABe2025: social action recognition improves when mice are processed as interacting agents rather than concatenated trajectories.

### 3. Fast temporal dynamics
A temporal encoder operates on each socially enriched mouse token. Benchmark a compact GRU/TCN against a Squeezeformer/Transformer. The purpose is not merely classification: it must predict masked frames/events and multiple future horizons.

### 4. Event and motif tokenizer
Maintain both continuous dynamics and a discrete behavioral vocabulary. Keypoint-MoSeq/VAME-like unsupervised motifs are useful as a tokenizer, but the canonical event ontology is directed:
agent, target, action, social content, outcome, context.

The present 5-event SOE world becomes one specialized slice of this larger event language.

### 5. Slow social-state memory
Use separate recurrent memory for:
- recent action/outcome history;
- minutes-scale social efficacy/reliability;
- social need/satiety;
- identity/familiarity and relationship history;
- rank/opponent capability;
- cross-day retained priors.

Do not force these timescales into one GRU hidden vector. The present SOE memory-horizon result already shows useful history over tens of trials.

### 6. Neural/social alignment
Use a **separate neural-dynamics stream by default**, aligned to but not assumed identical to the behavioral/social world state. External 13-region multifiber leave-one-animal-out tests show that current neural state robustly helps predict future neural state, whereas its increment for the next coarse social behavior is not stable across animals. The default behavioral policy therefore reads from the social core; neural-to-behavior fusion remains an optional diagnostic gate that must earn its way in with held-animal evidence.

Neural targets include:
- VTA DA social policy / APE / social RPE / credit;
- 13-region social-behavior-network photometry;
- CA2 identity/familiarity geometry;
- future Neuropixels/miniscope datasets.

Use CEBRA-like contrastive consistency and future-neural prediction as auxiliary objectives, while retaining generative social future prediction as the main world-model objective.

### 7. Intervention/action tokens
Interventions are explicit actions on the world: JAWS, optogenetic pattern, chemo, sensory block. The latent transition is conditioned on the intervention token and evaluated against no-action, wrong-action and shuffled-action controls.

### 8. Multimodal social communication
Add synchronized USV/audio, olfactory/social identity and tactile-contact channels when available. Missing modalities use masks and modality dropout so the core model can run on pose-only datasets.

## External architecture validation already completed
**Directed relation graph is required.** On the official CalMS21 animal-identity split (70 train, 19 unseen test animals), a quick deep SWM screen with the same training budget shows that true synchronized partner/relation state improves future-behavior NLL over resident-only state in 19/19 animals at ~0.4 s and ~0.8 s, and remains significant at ~2 s. Replacing the partner/relation stream with a within-animal time-shifted control gives nearly the same deficit as removing the partner, showing that the gain depends on the correct moment-by-moment relation rather than extra dimensions.

**Neural state is not the behavioral state by default.** In the 13-region social-behavior-network dataset, a fast leave-one-animal-out gate finds no stable neural increment for the next coarse social behavior, while current neural state improves future neural prediction in every evaluable animal. A shallow SWM quick screen reaches the same qualitative conclusion. This motivates a protected social/behavior core plus a neural auxiliary dynamics stream.

These are architecture-selection results, not final claims of external-pretraining transfer into SOE. That promotion is reserved for Stage30.

## Pretraining objectives
Use a weighted multi-objective curriculum rather than one supervised label loss:
- masked pose/keypoint reconstruction;
- masked agent/target identity prediction;
- relative geometry / TREBA-style expert attribute decoding;
- next-action and next-target prediction;
- next social-content/outcome prediction;
- future latent prediction at 0.5 s, 2 s, 10 s and event-scale horizons;
- cross-agent prediction: partner future from self+relation state and vice versa;
- contrastive identity/familiarity consistency;
- long-memory retrieval across separated encounters;
- neural-behavior contrastive alignment when neural data exist;
- intervention-conditioned future likelihood;
- closed-loop multi-step rollout.

## Mouse-first data curriculum
P0 datasets currently registered: {", ".join(atlas["priority_datasets"])}.

Recommended order:
1. MABe2025 + CalMS21 + MABe22 for broad social geometry/action pretraining.
2. Current SOE to teach observation, information content, value, credit and multi-step social foraging.
3. VTA social-RPE and 13-region multifiber datasets for neural alignment.
4. STFP for social-information-to-food-memory transfer.
5. CA2/social-memory and USV datasets for identity/familiarity and communication.
6. Cross-species datasets only after the mouse model is stable.

## Required evaluation hierarchy
A model is not promoted because its training loss improves. It must pass:
- held-animal;
- held-session;
- held-lab/domain;
- held-partner/identity where possible;
- social-content shuffle;
- wrong-social / no-social controls;
- future rollout against Markov, current-state MLP and recurrent controls;
- few-shot adaptation versus scratch;
- intervention true-vs-no-action, true-vs-wrong-action and shuffled-action;
- neural alignment on independent animals/datasets.

## Immediate engineering targets
1. Build a canonical adapter schema for MABe2025, CalMS21, MABe22 and SOE.
2. Pretrain an egocentric relational encoder using pose + pair geometry + masked/future objectives.
3. Add hierarchical fast/slow memory and the current SOE efficacy/credit heads.
4. Test whether external mouse pretraining improves held-SOE animals versus training from scratch.
5. Test whether SOE-trained slow-state heads improve STFP/VTA-social-RPE targets.
6. Only then scale model width/depth.

## Claim discipline
“World-best” should mean **broadest mouse-social state coverage + strongest held-domain transfer + longest validated memory + explicit causal intervention + neural grounding**, not simply the highest classifier F-score on one benchmark.
"""
(DOCS/"SOCIAL_WORLD_FOUNDATION_BLUEPRINT_v1_20261006.md").write_text(md, encoding="utf-8")

print(json.dumps({
  "datasets":len(datasets),
  "models":len(models),
  "priors":len(priors),
  "ontology":len(ontology),
  "outputs":[
    "data/SOCIAL_WORLD_DATASET_REGISTRY_v1.csv",
    "data/SOCIAL_WORLD_MODEL_ZOO_v1.csv",
    "data/SOCIAL_WORLD_BIOLOGICAL_PRIORS_v1.csv",
    "data/SOCIAL_WORLD_STATE_ONTOLOGY_v1.csv",
    "data/SOCIAL_WORLD_FIELD_ATLAS_v1.json",
    "docs/SOCIAL_WORLD_FOUNDATION_BLUEPRINT_v1_20261006.md"
  ]
}, indent=2))