# Lecture 10 Student Guide — CNN Fundamentals

## What you should be able to do

- Compute a 2D cross-correlation by hand.
- Calculate convolution and pooling output shapes.
- Count trainable parameters in a convolutional layer.
- Trace `[N,C,H,W]` tensors through a compact CNN.
- Distinguish translation equivariance from invariance.
- Design an evaluation split that tests the intended structural claim.

## Essential formulas

For one spatial dimension:

```text
n_out = floor((n + 2p - d(k - 1) - 1) / s) + 1
```

For an ordinary `Conv2d` layer with bias:

```text
parameters = C_out × C_in × kH × kW + C_out
```

PyTorch tensor contract:

```text
input   [N, C_in, H, W]
weight  [C_out, C_in / groups, kH, kW]
bias    [C_out]
output  [N, C_out, H_out, W_out]
```

## Concept map

- Locality controls which input region affects one output.
- Parameter sharing reuses a detector at many locations.
- Padding determines boundary treatment.
- Stride controls sampling density.
- Channels determine how measurements at the same location are mixed.
- Pooling summarizes local regions and reduces resolution.
- A receptive field is the input region that can affect a unit.

## Evidence from the lecture experiment

Both the MLP and CNN achieved 100% validation accuracy on central bar positions. On non-overlapping boundary positions, the reference MLP achieved 0% and the CNN achieved 100%. The comparison uses similar parameter counts and the same training protocol.

This result shows why a controlled shift can reveal an inductive-bias advantage that ordinary validation misses. It is evidence for this mechanism and protocol, not a universal rule that CNNs always win.

## Common mistakes

- Supplying NHWC when the model expects NCHW.
- Forgetting bias terms in parameter counts.
- Counting batch size as a model parameter.
- Applying softmax before `CrossEntropyLoss`.
- Tuning on the test set.
- Claiming invariance without evaluating an appropriate transformation split.
