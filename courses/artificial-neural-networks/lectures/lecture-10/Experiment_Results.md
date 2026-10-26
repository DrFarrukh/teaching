# SE-801 Lecture 10 Experiment Results

## Protocol

- Seed: `20261019`
- Images: 16 × 16, one channel
- Classes: vertical and horizontal bars with noise and variable intensity
- Training and validation positions: columns or rows 4–10
- Frozen shifted-test positions: 1, 2, 13, and 14
- Selection: lowest validation cross-entropy over 60 epochs
- Both models use the same split, loss, epoch budget, and test-release rule

## Verification

- Manual cross-correlation versus `torch.nn.functional.conv2d` maximum error: `0.0`
- MLP parameters: `1,038`
- CNN parameters: `982`

| Model | Validation accuracy | Shifted-test accuracy | Shifted-test loss |
|---|---:|---:|---:|
| MLP | 100.0% | 0.0% | 7.8809 |
| CNN | 100.0% | 100.0% | 0.0003 |

## Interpretation boundary

The experiment isolates a controlled translation shift in synthetic images. It shows
that the convolutional architecture transfers the learned local orientation detector
to positions excluded from training, while the compact MLP does not. It does not
establish universal CNN superiority, natural-image performance, robustness to other
shifts, or deployment performance.
