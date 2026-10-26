# Lecture 7 Data Dictionary

The classification experiment generates independent three-class spiral splits. The quadratic experiment evaluates a known two-dimensional objective. Batch-gradient variability uses fixed parameters and repeated sampled subsets of the training split.

## Common fields

| Field | Meaning |
|---|---|
| `features` | Floating-point model inputs |
| `targets` | Integer class indices |
| `split` | Independent training, validation, or test membership |
| `seed` | Registered random seed used to generate or sample data |
| `history` | Per-epoch loss and accuracy records |

## Generated outputs

- `outputs/experiment_results.json`: machine-readable metrics and protocol
- `outputs/*.png`: notebook evidence plots
- `outputs/*.pt`: model or checkpoint files when the lecture requires them

The synthetic data support mechanism checks. They do not establish performance on a real deployment population.
