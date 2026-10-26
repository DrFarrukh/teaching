# Synthetic Orientation Dataset — Data Dictionary

The lecture experiment generates all samples locally; no external dataset is downloaded.

| Field | Type / shape | Meaning |
|---|---|---|
| `image` | float32, `[1,16,16]` | Grayscale synthetic image after noise and bar insertion |
| `label` | integer | `0` for vertical bar, `1` for horizontal bar |
| `orientation` | categorical | Human-readable class identity: vertical or horizontal |
| `position` | integer | Column for a vertical bar or row for a horizontal bar |
| `split` | categorical | `train`, `validation`, or `shifted_test` |
| `seed` | integer | Deterministic generation seed; reference run uses `20261019` |

## Split definition

| Split | Samples | Allowed positions | Use |
|---|---:|---|---|
| Train | 800 | central positions `4..10` | Gradient updates |
| Validation | 200 | central positions `4..10` | Checkpoint selection and reporting |
| Shifted test | 200 | boundary positions `{1,2,13,14}` | One-time translation-transfer evaluation |

## Generation controls

- Image size: 16 × 16.
- One class-defining bright bar per image.
- Orientation and position are controlled explicitly.
- Background noise and bar intensity vary independently.
- Classes are balanced within each split.
- Central and shifted-test position sets do not overlap.

## Leakage boundary

The shifted-test samples are not used for training, early stopping, checkpoint selection, or architecture tuning in the reference protocol.
