# Lecture 9 Experiment Results

## Protocol

- Custom `ResearchMLP` with a residual block, dropout, and one registered buffer.
- Synthetic four-feature, three-class data with 540 training, 180 validation, and 180 test examples.
- Adam, learning rate 0.01, batch size 60, ten epochs, and `num_workers=0`.
- Exact-resume reference executed on CPU.

## Module and loader checks

- Trainable parameters: 1395
- Fresh loaders with equal generator state produced the same first order: True
- Advancing one generator changed its next order: True

## Serialization checks

- Weight reload maximum prediction error: `0.000e+00`
- Weight file size: 9552 bytes
- Interrupted versus uninterrupted prediction error: `0.000e+00`
- Maximum state-tensor error: `0.000e+00`
- Maximum recorded-history error: `0.000e+00`
- Final test accuracy: 100.00%
- Resume-checkpoint size: 37844 bytes

## Claim boundary

Exact equality applies to the recorded single-thread CPU reference. Different hardware, kernels, worker counts, or software versions can change floating-point execution and determinism.
