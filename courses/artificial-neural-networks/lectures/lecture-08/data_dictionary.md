# Lecture 8 Data Dictionary

The experiment generates independent three-class Gaussian splits with four features. Training-only standardization transforms validation and test data. A scratch tensor implementation and an nn.Module share copied parameters.

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
