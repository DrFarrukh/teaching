# SE-801 Lecture 6 Backpropagation, Initialization, and Stable Training

Student-facing slide manuscript. Slides 1–40 form the core route; Slides 41–42 are reserve material. Corresponds to `Lecture_06_Board_and_Speaking_Notes.md` and notebook `ANN_Lec_6.ipynb`.

---

## Slide 1 Backpropagation, Initialization, and Stable Training

- SE-801 Artificial Neural Networks
- Lecture 6
- Dr. Muhammad Farrukh Qureshi
- PNEC, NUST

---

## Slide 2 The Deep Learning Training Paradox

- In Lecture 5, we saw that stacked nonlinear layers form universal function approximators.
- Yet historically, networks deeper than 2 or 3 layers refused to learn when trained with gradient descent.
- Mathematical expressivity means nothing if gradient signals cannot propagate backwards across layers.

---

## Slide 3 Learning Outcomes for Today

- Derive reverse-mode automatic differentiation on forward computational graphs.
- Formulate exact matrix backpropagation equations and track tensor dimensions for batches.
- Diagnose gradient pathologies: vanishing gradients, exploding gradients, and symmetry collapse.
- Derive variance-preserving initializations (Xavier/Glorot and He/Kaiming).
- Implement inverted dropout and enforce the `model.train()` vs `model.eval()` contract.

---

## Slide 4 Computational Graphs: Forward vs Backward

- Every mathematical expression in PyTorch is represented as a directed acyclic graph (DAG).
- Forward pass: Computes output activations and evaluates the objective loss scalar.
- Backward pass: Reverses direction, propagating gradients via local chain rules.
- Crucial memory cost: Intermediate activations must be cached in GPU/RAM during the forward pass.

---

## Slide 5 Scalar Example: Logistic Loss Computational Graph

- Function: $L = \ln(1 + \exp(-z))$ where $z = w x + b$.
- Intermediate nodes: $z \to -z \to \exp(-z) \to 1 + \exp(-z) \to \ln(\cdot)$.
- Each node computes a local scalar derivative.
- PyTorch creates dynamic graphs during execution and frees intermediate nodes after `backward()`.

---

## Slide 6 The Scalar Chain Rule Trace

- Forward evaluation ($x=1.5, w=0.8, b=-0.4$):
  - $z = 0.8(1.5) - 0.4 = 0.8$
  - $L = \ln(1 + e^{-0.8}) \approx 0.3711$
- Backward chain rule:
  - $\frac{\partial L}{\partial z} = \sigma(z) - 1 = 0.6900 - 1 = -0.3100$
  - $\frac{\partial L}{\partial w} = \frac{\partial L}{\partial z} \cdot x = -0.3100 \times 1.5 = -0.4650$
  - $\frac{\partial L}{\partial b} = \frac{\partial L}{\partial z} \cdot 1 = -0.3100$
- Verified: PyTorch Autograd produces identical gradients to machine precision.

---

## Slide 7 Moving to Vectorized Batch Computations

- Training on single examples is slow and introduces high variance into gradient updates.
- In batch mode, $N$ independent examples pass through the network simultaneously.
- Mini-batch matrix formulation:
  - Input: $X \in \mathbb{R}^{N \times d_{\text{in}}}$
  - Hidden preactivations: $Z^{(1)} \in \mathbb{R}^{N \times d_h}$
  - Hidden representations: $H^{(1)} \in \mathbb{R}^{N \times d_h}$
  - Output logits: $Z^{(2)} \in \mathbb{R}^{N \times d_{\text{out}}}$

---

## Slide 8 Two-Layer MLP Forward Formulation

- Layer 1 affine transformation:
  $$Z^{(1)} = X W^{(1)} + \mathbf{1} (b^{(1)})^T$$
- Layer 1 nonlinear activation:
  $$H^{(1)} = \text{ReLU}(Z^{(1)}) = \max(0, Z^{(1)})$$
- Layer 2 affine transformation:
  $$Z^{(2)} = H^{(1)} W^{(2)} + \mathbf{1} (b^{(2)})^T$$
- Softmax output probabilities:
  $$P_{i, k} = \frac{\exp(Z_{i, k}^{(2)})}{\sum_{j=1}^{d_{\text{out}}} \exp(Z_{i, j}^{(2)})}$$

---

## Slide 9 The Mean Cross-Entropy Loss Objective

- For true class labels $y \in \{0, \dots, C-1\}^N$:
  $$L = -\frac{1}{N} \sum_{i=1}^N \ln P_{i, y_i}$$
- Log-sum-exp trick: In implementation, compute $\ln \sum \exp(z_j)$ stably by shifting by $\max(z)$.
- Cross-entropy penalizes confident wrong predictions with severe loss gradients.

---

## Slide 10 Derivation: Output Layer Error Signal

- Let error tensor $\Delta^{(2)} \equiv \frac{\partial L}{\partial Z^{(2)}}$.
- For sample $i$ and class $k$:
  $$\frac{\partial L}{\partial Z_{i, k}^{(2)}} = \frac{1}{N} (P_{i, k} - \mathbb{I}(y_i = k))$$
- Matrix form:
  $$\Delta^{(2)} = \frac{1}{N} (P - Y_{\text{onehot}}) \in \mathbb{R}^{N \times d_{\text{out}}}$$
- Intuition: The gradient is simply the model's probability error scaled by batch size $N$.

---

## Slide 11 Derivation: Output Weight and Bias Gradients

- Applying the matrix chain rule:
  $$\frac{\partial L}{\partial W^{(2)}} = (H^{(1)})^T \Delta^{(2)} \in \mathbb{R}^{d_h \times d_{\text{out}}}$$
  $$\frac{\partial L}{\partial b^{(2)}} = \sum_{i=1}^N \Delta_{i, :}^{(2)} \in \mathbb{R}^{d_{\text{out}}}$$
- Check dimensions:
  - $(H^{(1)})^T$ is $[d_h \times N]$
  - $\Delta^{(2)}$ is $[N \times d_{\text{out}}]$
  - Matrix product is $[d_h \times d_{\text{out}}]$ — matches $W^{(2)}$ exactly!

---

## Slide 12 Derivation: Hidden Layer Error Backpropagation

- Upstream gradient with respect to hidden activations:
  $$\frac{\partial L}{\partial H^{(1)}} = \Delta^{(2)} (W^{(2)})^T \in \mathbb{R}^{N \times d_h}$$
- Propagating through the ReLU nonlinearity:
  $$\Delta^{(1)} \equiv \frac{\partial L}{\partial Z^{(1)}} = \left(\frac{\partial L}{\partial H^{(1)}}\right) \odot \mathbb{I}(Z^{(1)} > 0)$$
- Hadamard product ($\odot$): Gradients pass through unattenuated if $Z^{(1)} > 0$; blocked completely if $Z^{(1)} \le 0$.

---

## Slide 13 Derivation: First Layer Parameter Gradients

- Parameter gradients for Layer 1:
  $$\frac{\partial L}{\partial W^{(1)}} = X^T \Delta^{(1)} \in \mathbb{R}^{d_{\text{in}} \times d_h}$$
  $$\frac{\partial L}{\partial b^{(1)}} = \sum_{i=1}^N \Delta_{i, :}^{(1)} \in \mathbb{R}^{d_h}$$
- Dimension alignment:
  - $X^T$ is $[d_{\text{in}} \times N]$
  - $\Delta^{(1)}$ is $[N \times d_h]$
  - Result is $[d_{\text{in}} \times d_h]$ — exactly the shape of $W^{(1)}$.

---

## Slide 14 Mathematical Verification: Scratch vs Autograd

- In our double-precision benchmark, we compared manual matrix formulas against PyTorch `backward()`:
  - Max error on $W^{(1)}$: $1.21 \times 10^{-16}$
  - Max error on $W^{(2)}$: $1.94 \times 10^{-16}$
  - Max error on biases: $< 1.11 \times 10^{-16}$
- Conclusion: Autograd does not approximate; it executes exact symbolic chain rule arithmetic.

---

## Slide 15 The Vanishing Gradient Problem

- What happens when a network has $L=10$ or $L=20$ layers?
- Gradient at layer 1 involves a product of $L$ Jacobian matrices:
  $$\frac{\partial L}{\partial Z^{(1)}} = \frac{\partial L}{\partial Z^{(L)}} \prod_{l=1}^{L-1} W^{(l+1)} \text{diag}(\phi'(Z^{(l)}))$$
- If the terms in this product are consistently smaller than 1, the gradient shrinks exponentially towards zero.

---

## Slide 16 The Saturation Trap of Sigmoidal Activations

- Sigmoid: $\sigma'(z) = \sigma(z)(1 - \sigma(z)) \le 0.25$ (maximum achieved at $z=0$).
- Tanh: $\tanh'(z) = 1 - \tanh^2(z) \le 1.0$ (maximum at $z=0$).
- When $|z| \gg 0$, $\sigma'(z) \to 0$ and $\tanh'(z) \to 0$.
- In a 10-layer Sigmoid network, gradient norm shrinks by $(0.25)^{10} \approx 10^{-6}$.
- Early layers stop learning completely: parameters remain frozen near initial random values.

---

## Slide 17 Why ReLU Changed Deep Learning

- Rectified Linear Unit: $\text{ReLU}(z) = \max(0, z)$.
- Derivative: $\phi'(z) = 1$ for all $z > 0$.
- Advantage: No gradient saturation for positive activations; gradient passes through with constant magnitude 1.
- Drawback: "Dying ReLU" — if a neuron's preactivations become negative for all data, its gradient is permanently 0.

---

## Slide 18 Symmetry Collapse Under Zero Initialization

- What if we initialize all weights to zero ($W = \mathbf{0}, b = \mathbf{0}$)?
- In the forward pass, all neurons in a hidden layer compute identical values.
- In the backward pass, all neurons receive identical gradient updates.
- Symmetry is never broken: regardless of width $d_h$, the entire layer acts as a single neuron.
- Fundamental rule: Weights must be initialized with random asymmetries.

---

## Slide 19 Naive Random Initialization Pitfalls

- If random initialization is required, why not standard Gaussian $\mathcal{N}(0, 1)$?
- Consider linear sum: $y = \sum_{j=1}^{d_{\text{in}}} w_j x_j$.
- If $w_j \sim \mathcal{N}(0, 1)$ and $x_j \sim \mathcal{N}(0, 1)$ with $d_{\text{in}} = 256$:
  $$\text{Var}(y) = d_{\text{in}} \text{Var}(w) \text{Var}(x) = 256 \times 1 \times 1 = 256$$
- After 4 layers, variance explodes: $256^4 \approx 4.3 \times 10^9$ (Exploding activations / NaNs).
- If $\sigma = 0.01$, variance collapses: $0.025^4 \approx 10^{-7}$ (Vanishing signals).

---

## Slide 20 Break

- 20 minutes break.
- Up next: Variance-preserving initialization (Xavier and Kaiming) and regularization via Inverted Dropout.

---

## Slide 21 The Principle of Variance Preservation

- Goal: Maintain the variance of activations in the forward pass, and the variance of gradients in the backward pass.
  $$\text{Var}(y^{[l]}) = \text{Var}(y^{[l-1]}), \quad \text{Var}\left(\frac{\partial L}{\partial z^{[l-1]}}\right) = \text{Var}\left(\frac{\partial L}{\partial z^{[l]}}\right)$$
- For a linear layer with zero-mean inputs:
  $$\text{Var}(y) = d_{\text{in}} \text{Var}(w) \text{Var}(x)$$
- Forward pass stability requires $\text{Var}(w) = \frac{1}{d_{\text{in}}}$.
- Backward pass stability requires $\text{Var}(w) = \frac{1}{d_{\text{out}}}$.

---

## Slide 22 Xavier / Glorot Initialization (2010)

- Harmonic mean compromise for symmetric activations (Linear, Tanh):
  $$\text{Var}(w) = \frac{2}{d_{\text{in}} + d_{\text{out}}}$$
- Uniform distribution:
  $$W \sim \mathcal{U}\left(-\sqrt{\frac{6}{d_{\text{in}} + d_{\text{out}}}}, \sqrt{\frac{6}{d_{\text{in}} + d_{\text{out}}}}\right)$$
- Normal distribution:
  $$W \sim \mathcal{N}\left(0, \frac{2}{d_{\text{in}} + d_{\text{out}}}\right)$$
- Works exceptionally well for Sigmoid and Tanh, but fails for ReLU.

---

## Slide 23 Why ReLU Requires Kaiming / He Initialization

- ReLU sets all negative preactivations to zero.
- For symmetric zero-mean preactivations, exactly half the distribution is removed.
  $$\mathbb{E}[(\text{ReLU}(z))^2] = \frac{1}{2} \text{Var}(z)$$
- Consequently, propagating through a Linear + ReLU layer halves the signal variance:
  $$\text{Var}(y) = \frac{d_{\text{in}}}{2} \text{Var}(w) \text{Var}(x)$$
- To compensate for the 50% loss of signal, we must double the weight variance!

---

## Slide 24 Kaiming (He) Normal Initialization (2015)

- Setting $\frac{d_{\text{in}}}{2} \text{Var}(w) = 1$ yields:
  $$\text{Var}(w) = \frac{2}{d_{\text{in}}} \implies \sigma_w = \sqrt{\frac{2}{d_{\text{in}}}}$$
- In PyTorch:
  ```python
  torch.nn.init.kaiming_normal_(linear.weight, nonlinearity='relu')
  torch.nn.init.zeros_(linear.bias)
  ```
- This single formula made training very deep ReLU networks (such as 100-layer ResNets) reliably possible.

---

## Slide 25 Empirical Verification: Variance Across 8 Layers

- We measured activation distributions across 8 hidden layers (width 256):
  - Naive Small ($\sigma=0.05$): Variance collapses to $0$ by layer 3 (signal dead).
  - Naive Large ($\sigma=0.35$): Variance explodes to $> 100$ (numerical instability).
  - Xavier Normal: Variance steadily shrinks across layers under ReLU.
  - Kaiming Normal: Maintains healthy, non-degenerate variance across all 8 layers.

---

## Slide 26 Regularization: The Overfitting Threat in Deep MLPs

- As depth and width grow, parameter capacity increases dramatically.
- An overparameterized MLP easily memorizes noisy training points.
- How can we regularize deep networks without restricting structural expressivity?
- Weight decay ($L_2$) shrinks weight magnitudes.
- Dropout (Srivastava et al., 2014) regularizes by preventing feature co-adaptation.

---

## Slide 27 The Dropout Intuition: Co-Adaptation Prevention

- In standard training, neurons can develop complex co-dependencies where one neuron corrects another's error.
- Dropout randomly removes a subset of neurons during each training step with probability $p$.
- Each neuron must learn features that are useful in random combinations with other neurons.
- Acts as an implicit ensemble over an exponential number of sub-networks.

---

## Slide 28 Inverted Dropout Formulation

- Standard dropout requires scaling activations by $(1-p)$ at inference time.
- Modern frameworks use **Inverted Dropout** during training:
  $$M_{i, j} \sim \text{Bernoulli}(1 - p)$$
  $$\tilde{H}_{i, j} = \frac{H_{i, j} M_{i, j}}{1 - p}$$
- Unconditional expectation is preserved during training:
  $$\mathbb{E}[\tilde{H}_{i, j}] = (1 - p) \cdot \frac{H_{i, j}}{1 - p} + p \cdot 0 = H_{i, j}$$
- Consequence: Inference pass requires zero scaling — exactly identity!

---

## Slide 29 The PyTorch Training vs Evaluation Contract

- Dropout behaves fundamentally differently during training vs testing:
  - Training: Random masking with $\frac{1}{1-p}$ scaling.
  - Evaluation: Identity mapping (all units active, unscaled).
- In PyTorch, you must explicitly declare model mode:
  ```python
  model.train()  # Activates dropout and batchnorm updates
  # ... training steps ...
  model.eval()   # Freezes running statistics, deactivates dropout
  with torch.no_grad():
      # ... validation / test evaluation ...
  ```

---

## Slide 30 The Diagnostic Benchmark: 3-Ring Concentric Data

- 2D nonlinear multi-class classification benchmark.
- 3 concentric circular rings ($r \in \{0.8, 1.8, 2.8\}$) with Gaussian radial jitter.
- 1,200 total samples: 60% train (720), 20% validation (240), 20% test (240).
- Balanced across all 3 classes (no class imbalance bias).
- Linear classifiers fail completely; requires a multi-layer nonlinear network.

---

## Slide 31 The DeepMLP Architecture

- 4-layer fully connected network:
  $$\text{Input (2)} \to \text{Linear(64)} \to \text{ReLU} \to \text{Dropout} \to \text{Linear(64)} \to \text{ReLU} \to \text{Dropout} \dots \to \text{Linear(3)}$$
- Total parameters: 8,707 trainable weights and biases.
- Controlled comparison: Keep dataset split, optimizer, learning rate ($\eta = 0.03$), batch size ($64$), and epoch budget ($80$) strictly identical.

---

## Slide 32 Diagnostic Comparison: Small vs Large vs Kaiming

- **Naive Small ($\sigma=0.01$):**
  - Validation accuracy stays at 33.75% (random guessing!).
  - Layer 1 gradient norm: $1.8 \times 10^{-5}$ (gradient starvation).
- **Naive Large ($\sigma=1.20$):**
  - Rapid convergence, reaches 100% validation accuracy, but vulnerable to saturation in deeper networks.
- **Kaiming Normal:**
  - Stable, smooth loss descent, reaching 100% validation accuracy with well-conditioned gradient flow ($10^{-1}$).

---

## Slide 33 Examining First-Layer Gradient Flow

- Why did Naive Small fail?
- The first-layer gradient norm $\|\nabla_{W^{(1)}} L\|_2$ remained stuck at $10^{-5}$ throughout all 80 epochs.
- The downstream weights were too small to produce substantial error signals back to layer 1.
- Lesson: Networks do not fail because gradient descent broke; they fail because gradients never arrived!

---

## Slide 34 Regularization Results: With vs Without Dropout

- Comparing No-Dropout ($p=0$) vs Inverted Dropout ($p=0.25$):
  - No-Dropout: Reaches training loss $0.0031$, test accuracy 100.0%.
  - With Dropout ($p=0.25$): Training loss higher ($0.2845$), test accuracy $94.17\%$.
- On clean low-dimensional synthetic data, dropout adds variance.
- On high-dimensional, noisy data, dropout prevents memorization and closes the generalization gap.

---

## Slide 35 Diagnostic Debugging: Bug 1 — Missing zero_grad()

- Common beginner mistake:
  ```python
  loss = criterion(model(x), y)
  loss.backward()
  # Missing: optimizer.zero_grad()!
  ```
- PyTorch **accumulates** gradients in `.grad` by default.
- Gradient norm grows linearly with each batch ($0.40 \to 0.79 \to 1.19 \to 1.59$).
- Effective learning rate unintentionally explodes!

---

## Slide 36 Diagnostic Debugging: Bug 2 — Forgetting model.eval()

- If `model.eval()` is omitted during testing:
  - Dropout remains active during inference.
  - Passing the exact same test batch 3 times gives 3 completely different prediction vectors!
- Test evaluation becomes stochastic and non-deterministic.
- Fix: Always call `model.eval()` and wrap in `with torch.no_grad():`.

---

## Slide 37 Diagnostic Debugging: Bug 3 — Dead ReLUs

- When large negative gradients push weights such that a neuron's preactivation is always negative:
  $$Z_{i, j} < 0 \quad \forall i \in \{1, \dots, N\}$$
- Then $\text{ReLU}'(Z_{i, j}) = 0$, so no gradient ever updates that neuron again.
- The neuron is permanently dead.
- Solutions: Leaky ReLU ($\phi(z) = \max(\alpha z, z)$), proper Kaiming initialization, lower learning rate.

---

## Slide 38 Final Frozen Test Set Evaluation

- Protocol frozen before inspecting held-out test data:
  - Naive Small Init: Test Loss = 1.1089, Test Accuracy = 26.67% (Failure).
  - Naive Large Init: Test Loss = 0.0047, Test Accuracy = 100.00%.
  - Kaiming Normal (No Drop): Test Loss = 0.0194, Test Accuracy = 100.00%.
  - Kaiming Normal (Dropout 0.25): Test Loss = 0.3268, Test Accuracy = 94.17%.
- Validates that proper initialization is a prerequisite for network convergence.

---

## Slide 39 Summary of Practical Deep Learning Rules

1. **Always use Kaiming initialization for ReLU networks** (or Xavier for Tanh).
2. **Never initialize weights to constant values or zeros**.
3. **Always call `zero_grad()` before `loss.backward()`**.
4. **Always toggle between `model.train()` and `model.eval()`**.
5. **Monitor gradient norms across layers** when deep networks fail to converge.

---

## Slide 40 Looking Ahead: Week 7 Optimization Algorithms

- Today we fixed gradient *signal propagation* and *initialization*.
- But basic SGD moves slowly in ill-conditioned ravines and plateaus.
- Next week (Week 7):
  - Momentum, RMSprop, and Adam.
  - Learning rate schedules and optimization dynamics across loss landscapes.

---

## Slide 41 Reserve 1: Layer-by-Layer Gradient Flow Bar Chart

- Healthy backpropagation maintains gradient norms within the same order of magnitude across all layers.
- Diagnostic check: Compare Frobenius norm of weights from `fc1` through `fc4`.
- Under Kaiming initialization, gradient signals remain balanced throughout the entire network depth.

---

## Slide 42 Reserve 2: Leaky ReLU vs Parametric ReLU (PReLU)

- To eliminate dead ReLUs, allow a small slope $\alpha > 0$ for $z < 0$:
  $$\text{Leaky ReLU}(z) = \max(\alpha z, z), \quad \alpha \approx 0.01$$
- Local derivative for $z < 0$ is $\alpha$ rather than 0.
- PReLU treats $\alpha$ as a learnable parameter optimized via backpropagation.
