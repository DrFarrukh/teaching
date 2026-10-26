# Lecture 8 Experiment Results

## Protocol

- Independent synthetic splits: 480 training, 165 validation, and 165 held-out test examples.
- Four features, three classes, and train-only standardization.
- A 4-12-3 ReLU MLP trained for 80 epochs with momentum SGD, learning rate 0.08, and batch size 48.
- Lowest validation cross-entropy selects the checkpoint.

## Scratch and module equivalence

- Maximum logit error: `0.000e+00`
- Scalar loss error: `0.000e+00`
- Maximum parameter-gradient error: `1.388e-17`

## Broadcasting counterexample

The faulty `[3,1] - [3]` operation produced shape `[3, 3]` and MSE `1.333333`. Matching the shapes produced MSE `0.0`.

## Selected model

- Parameter count: 99
- Selected epoch: 6
- Validation cross-entropy: 0.050197
- Test cross-entropy: 0.063310
- Test accuracy: 96.97%
- Balanced accuracy: 96.97%
- Test confusion matrix: `[[54, 1, 0], [3, 52, 0], [0, 1, 54]]`

## Claim boundary

The equivalence checks verify this forward and backward implementation on the tested tensors. The classification result describes one synthetic protocol and does not establish external performance.
