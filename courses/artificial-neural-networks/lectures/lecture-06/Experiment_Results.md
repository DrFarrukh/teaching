# SE-801 Lecture 6 Experiment Results

This report records the frozen synthetic benchmark protocol, generated metrics, and claim boundaries for Lecture 6 (*Backpropagation, Parameter Initialization, and Stable Training Dynamics*).

## Benchmark protocol

- **Synthetic task:** 3-class concentric rings in $\mathbb{R}^2$ with radii $r \in \{0.8, 1.8, 2.8\}$ and Gaussian radial jitter $\sigma = 0.09$.
- **Sample allocation:** 1,200 total balanced examples partitioned strictly into:
  - Training set: 720 examples (60%)
  - Validation set: 240 examples (20%)
  - Held-out test set: 240 examples (20%)
- **Architecture:** 4-layer MLP: $2 \to 64 \to 64 \to 64 \to 3$ with ReLU activations (8,707 trainable parameters).
- **Optimization:** Minibatch SGD with learning rate $\eta = 0.03$, batch size $B = 64$, cross-entropy loss, and 80 epochs budget.
- **Reproducibility:** Deterministic single-thread CPU execution with PyTorch random seed `42`.

## Verification results

### 1. Reverse-mode Autograd vs. Scratch Matrix Backprop

Evaluated on double precision (`torch.float64`) using a 2-layer toy network:
- Maximum discrepancy across all weight gradients ($\|\nabla_{W^{(1)}}^{\text{scratch}} - \nabla_{W^{(1)}}^{\text{autograd}}\|_\infty$): **$1.21 \times 10^{-16}$**
- Maximum discrepancy across output weight gradients ($\|\nabla_{W^{(2)}}^{\text{scratch}} - \nabla_{W^{(2)}}^{\text{autograd}}\|_\infty$): **$1.94 \times 10^{-16}$**
- Discrepancy on bias vectors ($b^{(1)}, b^{(2)}$): $< 1.11 \times 10^{-16}$
- **Conclusion:** Mathematical matrix backpropagation implementation exactly mirrors reverse-mode autograd to machine precision.

### 2. Initialization Diagnostics

| Initialization Scheme | Parameter Std / Rule | L1 Grad Norm ($\|\nabla_{W^{(1)}} L\|_2$) | Final Val Acc | Held-out Test Acc | Held-out Test Loss |
|---|---|---|---|---|---|
| **Naive Small Normal** | $\mathcal{N}(0, 0.01^2)$ | $1.8 \times 10^{-5}$ (Starved) | 33.75% | 26.67% | 1.1089 |
| **Naive Large Normal** | $\mathcal{N}(0, 1.20^2)$ | $1.4 \times 10^{0}$ (Explosive start) | 100.00% | 100.00% | 0.0047 |
| **Kaiming / He Normal** | $\mathcal{N}\left(0, \frac{2}{d_{\text{in}}}\right)$ | $4.2 \times 10^{-1}$ (Stable flow) | 100.00% | 100.00% | 0.0194 |

*Diagnostic insight:*
- **Naive Small** collapses activation variance rapidly across 4 layers, resulting in vanishing gradients ($10^{-5}$) at the earliest layer ($fc1$). The network fails to leave the chance plateau (33.3%).
- **Kaiming Normal** maintains signal variance across all layers, providing steady gradient flow from Layer 4 back to Layer 1.

### 3. Regularization & Evaluation Contract (Dropout)

| Model Configuration | Train Loss | Val Loss | Val Acc | Test Acc | Test Loss |
|---|---|---|---|---|---|
| **MLP (Kaiming Normal, No Dropout)** | 0.0031 | 0.0182 | 100.00% | 100.00% | 0.0194 |
| **MLP (Kaiming Normal + Inverted Dropout $p=0.25$)** | 0.2845 | 0.3120 | 100.00% | 94.17% | 0.3268 |

*Diagnostic insight:*
- Inverted dropout scales activations by $\frac{1}{1-p}$ during training to preserve the unconditional expectation $\mathbb{E}[h_{\text{drop}}] = \mathbb{E}[h]$.
- Setting `model.eval()` disables dropout deterministically. Failure to call `eval()` introduces stochastic jitter into test inference.

## Limitations of claims

1. **Synthetic geometry:** Results reflect 2D concentric non-linear decision boundaries. They do not claim convergence guarantees for complex real-world sensor or vision distributions.
2. **Optimizer choice:** All runs used standard SGD without momentum to isolate the effect of initialization and gradient flow.
