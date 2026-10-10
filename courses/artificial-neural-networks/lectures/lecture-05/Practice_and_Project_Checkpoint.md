# Lecture 5 Practice and Project Checkpoint

## Practice

These tasks extend the lecture's ungraded practice. They introduce no new assessment weight or deadline. A formal Assignment 2 can later use this work with the instructor's announced marking and submission requirements.

1. **Affine control:** remove ReLU from the copied scratch and framework models. Verify the effective affine weight and bias, then compare validation performance under the same split and training budget. Explain what parameter count can and cannot establish.
2. **Two equivalent MLPs:** implement a $2\to4\to2$ MLP with tensors and `nn.Sequential`. Copy the same initial tensors. Check logits, loss, gradients and one SGD update before training. Explain every weight transpose.
3. **An activation comparison:** replace ReLU with tanh while keeping data, width, initialization tensors, loss and budget fixed. Use validation evidence and report all registered initializations. Do not use test data to choose the activation.
4. **One scientific paragraph:** explain what the noisy XOR result shows about representation, optimization and generalization, with one limitation for each relevant claim.

Submit or retain the equations, relevant code, evidence tables and a brief explanation rather than only a screenshot of final accuracy. Student-controlled extensions should keep a separate held-out test set sealed until their own recipe is frozen.

## Two-page project proposal

Include:

- The research question and the decision or scientific comparison it serves.
- Dataset source, permissions/availability, target and observation unit.
- A defensible baseline and candidate model, with a reason for nonlinear capacity if proposed.
- Train/validation/test strategy tied to the intended generalization population, including subject/session/time boundaries where relevant.
- Metrics and error costs, with a reason for each main reported metric.
- A feasible computational plan: model size, hardware, training budget and reproducibility record.
- The strongest likely limitation and one specific check that could expose a misleading result.

The proposal should be specific enough to identify what data enters each split and what observation would weaken the proposed claim. Team size and submission date follow the instructor's existing project arrangements.
