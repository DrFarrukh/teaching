# Lecture 10 Practice and Project Checkpoint

## Practice A — Shape table

For input `[4,3,64,64]`, complete the shape trace:

```text
Conv2d(3,16,3,padding=1)
MaxPool2d(2)
Conv2d(16,32,5,padding=2,stride=2)
AdaptiveAvgPool2d((1,1))
flatten
Linear(32,10)
```

Report every output shape and the trainable parameters in each learned layer.

## Practice B — Controlled shift

Modify the synthetic generator so that training positions are on the left half and test positions are on the right half. Keep class balance, noise distribution, optimizer, epoch budget, and checkpoint rule unchanged. Report:

- validation accuracy;
- shifted-test accuracy;
- parameter count;
- at least one failure example;
- whether the evidence supports your transfer claim.

## Project checkpoint

Add the following to your course project record:

1. The structural assumption encoded by your model.
2. A complete tensor-shape trace for one batch.
3. Parameter counts for the main model and a simpler baseline.
4. A data split that tests the deployment claim rather than merely repeating the training distribution.
5. One observed or plausible failure mode.
6. A statement separating measured evidence from speculation.

## Submission standard

Your result must be reproducible from a fixed seed and a documented split. Do not use the test set for architecture selection, early stopping, or hyperparameter tuning.
