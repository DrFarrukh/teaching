# SE-801 Lecture 6 Concept Check

**Instructions:** Answer each of the five diagnostic questions below. This is an ungraded concept check to assess understanding of backpropagation, initialization, and training stability.

---

### Question 1: Matrix Shape Tracking
In a multilayer perceptron, the hidden activation matrix $H^{(1)}$ has shape $[64, 128]$ (corresponding to $N=64$ examples and $d_h=128$ hidden units). The upstream gradient with respect to output preactivations $\Delta^{(2)} \equiv \frac{\partial L}{\partial Z^{(2)}}$ has shape $[64, 10]$ (where $d_{\text{out}}=10$).

Write the exact matrix multiplication formula to compute $\frac{\partial L}{\partial W^{(2)}}$, and state its resulting dimension. Explain why the shapes must align in this specific orientation.

---

### Question 2: The Sigmoid Saturation Trap
Consider an 8-layer feedforward neural network using the standard sigmoid activation function $\sigma(z) = \frac{1}{1 + e^{-z}}$ at each layer.
1. What is the mathematical maximum of $\sigma'(z)$, and for what value of $z$ does it occur?
2. If all layers operate with preactivations near $|z| = 3.0$ where $\sigma'(z) \approx 0.045$, estimate the factor by which the loss gradient is attenuated when backpropagating from the final layer to the first hidden layer.

---

### Question 3: Symmetry Collapse
Suppose you initialize all weights $W$ and biases $b$ of an MLP to exactly zero ($W = \mathbf{0}, b = \mathbf{0}$).
Explain what happens to:
1. The hidden activations $h_j$ across neurons in the same layer during the forward pass.
2. The gradients $\frac{\partial L}{\partial W_{i, j}}$ during the backward pass.
Can gradient descent break this symmetry if training continues for 1,000 epochs?

---

### Question 4: Deriving the Factor of 2 in Kaiming Initialization
For a linear layer with independent weights and zero-mean inputs, the output variance satisfies $\text{Var}(y) = d_{\text{in}} \text{Var}(w) \text{Var}(x)$.
Explain mathematically why introducing a standard $\text{ReLU}(z) = \max(0, z)$ activation requires setting $\text{Var}(w) = \frac{2}{d_{\text{in}}}$ rather than $\frac{1}{d_{\text{in}}}$ to prevent activation variances from collapsing to zero across deep layers.

---

### Question 5: Inverted Dropout and Evaluation Pitfalls
1. Why does modern PyTorch use *inverted dropout* (multiplying by $\frac{1}{1-p}$ during the training pass) rather than scaling by $(1-p)$ at test time?
2. A junior engineer trains an MLP with `nn.Dropout(p=0.5)` and reports that identical test inputs produce fluctuating accuracy and differing predictions across runs. What single line of PyTorch code did they forget to execute, and why does that fix the issue?
