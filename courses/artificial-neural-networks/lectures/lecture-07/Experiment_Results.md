# Lecture 7 Experiment Results

## Protocol

- Three-class synthetic spiral data: 540 training, 180 validation, and 180 held-out test examples.
- Shared 2-32-32-3 tanh MLP initialization and identical batch-order seed.
- Eighty epochs with batch size 54.
- Learning rates: SGD 0.08, momentum SGD 0.05 with momentum 0.9, Adam 0.01.
- Lowest validation cross-entropy selects the checkpoint. The frozen test set is evaluated afterward.

## Gradient variability at one fixed parameter state

| Batch size | Mean relative deviation from full gradient | Mean cosine with full gradient |
|---:|---:|---:|
| 1 | 9.255 | 0.101 |
| 16 | 1.977 | 0.508 |
| 64 | 0.864 | 0.761 |
| 540 | 0.000 | 1.000 |

## Optimizer results

| Optimizer | Selected epoch | Validation CE | Test CE | Test accuracy |
|---|---:|---:|---:|---:|
| SGD | 80 | 0.780406 | 0.784232 | 51.67% |
| Momentum | 80 | 0.018139 | 0.017788 | 100.00% |
| Adam | 80 | 0.003954 | 0.003599 | 100.00% |

## Claim boundary

The reference run shows different learning dynamics under the registered settings. It does not establish a universal optimizer ranking. The learning rates are optimizer-specific choices, and the synthetic task is small.
