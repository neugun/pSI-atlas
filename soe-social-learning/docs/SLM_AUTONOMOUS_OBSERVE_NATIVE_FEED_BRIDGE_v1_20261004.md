# Autonomous SLM Observe -> native Feed hybrid bridge v1

Purpose: first strict intermediate closure before feeding is allowed to alter the transition world. The SLM Observe schedule and outcomes are autonomous/OOF; the 1-s physical state grid and native Feed labels remain replayed real behavior.

A Feed-hazard model is fit only on training animals using REAL previous-Observe timing/content. On held-out animals it is evaluated twice on identical decisions: (1) previous REAL Observe; (2) previous AUTONOMOUS-SLM generated Observe, with demonstrator-feeding content taken from the physical state at the generated observation opportunity.

This tests whether the Artificial SLM samples moments whose content can be translated by the empirically learned Observe->Feed bridge. It is not yet a fully autonomous Feed rollout.

## Coverage
common decisions = 105994; animals = 27; sessions = 54

## Summary
         model  n  logloss    brier  auc_feed
actual_content 27 0.253328 0.077094  0.819107
actual_recency 27 0.253740 0.077174  0.819361
  auto_content 27 0.252568 0.076947  0.821760
  auto_recency 27 0.253153 0.077062  0.821215

## Effects
                      comparison   metric  n  positive  mean_improvement  median_improvement  rank_biserial  p_one_sided
actual_content_vs_actual_recency  logloss 27        18          0.000412            0.000384       0.328042     0.070703
actual_content_vs_actual_recency    brier 27        18          0.000080            0.000076       0.306878     0.084907
actual_content_vs_actual_recency auc_feed 27        13         -0.000255           -0.000102      -0.079365     0.643011
    auto_content_vs_auto_recency  logloss 27        18          0.000585            0.000154       0.370370     0.047694
    auto_content_vs_auto_recency    brier 27        18          0.000115            0.000127       0.402116     0.034613
    auto_content_vs_auto_recency auc_feed 27        17          0.000544            0.000741       0.248677     0.134336
  auto_content_vs_actual_recency  logloss 27        19          0.001172            0.000850       0.539683     0.006505
  auto_content_vs_actual_recency    brier 27        19          0.000227            0.000205       0.523810     0.008095
  auto_content_vs_actual_recency auc_feed 27        16          0.002399            0.000704       0.396825     0.036570
  auto_content_vs_actual_content  logloss 27        15          0.000760            0.000323       0.137566     0.273009
  auto_content_vs_actual_content    brier 27        16          0.000147            0.000079       0.132275     0.280966
  auto_content_vs_actual_content auc_feed 27        15          0.002653            0.000694       0.211640     0.174164

## Direct generated-observation hazard
    window          metric  n  positive      mean    median  rank_biserial  p_one_sided
 age_le_3s feed_rate_delta 24        10  0.001020 -0.021021      -0.020000     0.539096
 age_le_3s  residual_delta 24        10 -0.012670 -0.022569      -0.153333     0.745617
age_le_10s feed_rate_delta 25        17  0.031294  0.021208       0.390769     0.045158
age_le_10s  residual_delta 25        14  0.018600  0.010044       0.267692     0.126052
age_le_30s feed_rate_delta 25        19  0.024420  0.019143       0.556923     0.006777
age_le_30s  residual_delta 25        15  0.012445  0.011386       0.384615     0.047867
age_le_60s feed_rate_delta 25        18  0.026455  0.024851       0.556923     0.006777
age_le_60s  residual_delta 25        15  0.015955  0.009860       0.366154     0.056746
