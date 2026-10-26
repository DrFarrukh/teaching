# SE-801 Lecture 6 Practice and Project Checkpoint

This guide connects the concepts of Lecture 6 to **Assignment 2** and the **Semester Project Proposal Milestone** (due Week 7 / Week 8).

---

## Part 1: Individual Implementation Practice (Assignment 2 Alignment)

Lecture 6 establishes the mathematical mechanics of backpropagation and the practical necessity of initialization and regularizers. Work through the following four implementation exercises in `ANN_Lec_6.ipynb` or an independent script:

### Exercise 1: Manual Backpropagation with Batch Normalization Preview
- Take the scratch 2-layer backpropagation engine from RUN 5.
- Add an element-wise scaling parameter $\boldsymbol{\gamma}$ and shifting parameter $\boldsymbol{\beta}$ to the hidden preactivation: $\tilde{Z}^{(1)} = \boldsymbol{\gamma} \odot Z^{(1)} + \boldsymbol{\beta}$.
- Derive and implement the matrix gradients $\frac{\partial L}{\partial \boldsymbol{\gamma}}$ and $\frac{\partial L}{\partial \boldsymbol{\beta}}$. Verify against PyTorch Autograd within $10^{-12}$ absolute tolerance.

### Exercise 2: Dying ReLU Diagnostic Hook
- Register a PyTorch forward hook on the hidden layers of `DeepMLP`:
  ```python
  def relu_hook(module, input, output):
      dead_ratio = (output == 0).float().mean().item()
      print(f"Layer {module} dead neuron fraction: {dead_ratio:.2%}")
  ```
- Train the network with an excessively large learning rate ($\eta = 0.5$) and observe how many neurons become permanently inactive ("dead ReLUs").

### Exercise 3: Gradient Norm Tracking Across Deeper Networks
- Construct an 8-layer MLP.
- Train it using:
  1. Xavier Normal with Tanh activations.
  2. Kaiming Normal with ReLU activations.
  3. Standard Normal ($\sigma=1.0$) with Sigmoid activations.
- Plot the ratio $\frac{\|\nabla_{W^{(1)}} L\|}{\|\nabla_{W^{(8)}} L\|}$ over training epochs. Confirm that Kaiming preserves a healthy ratio near $\mathcal{O}(10^{-1})$ to $\mathcal{O}(1)$ throughout optimization.

---

## Part 2: Semester Project Milestone (Week 7 Target)

In Week 7, each team of 2–3 students will commit their **baseline pipeline and verified data split** to their repository. Ensure your project repository satisfies:

1. **Deterministic Data Partition:**
   - A frozen split function with fixed seed saving sample indices to `splits/train_indices.csv`, `splits/val_indices.csv`, and `splits/test_indices.csv`.
   - Clear documentation of grouping variables (e.g., patient ID, session ID, sensor subject) to avoid data leakage.
2. **Simple Baseline Model:**
   - A non-neural baseline (e.g., logistic regression, ridge regression, or majority class predictor) evaluated on the frozen validation partition.
3. **Reproducible Pipeline:**
   - Single-command training script recording seed, configuration JSON, and checkpoint metrics.
   - Initial learning curves showing training and validation loss plotted on identical scales.
