# SE-801 Lecture 5 Concept Check

**Mode:** ungraded individual practice. Use selected questions in class or complete the sheet after the lecture. Explain your method and keep conceptual answers concise.

## 1 Affine composition

For a scalar input, $h=3x-2$ and $o=-2h+4$. Express $o$ directly as a function of $x$. Would stacking a third affine layer make the input-to-output map nonlinear? Explain.

## 2 One hidden-layer calculation

Use column vectors:

$$x=\begin{bmatrix}2\\-1\end{bmatrix},\quad W_1=\begin{bmatrix}1&1\\-1&2\end{bmatrix},\quad b_1=\begin{bmatrix}0\\1\end{bmatrix}.$$

Calculate $z=W_1x+b_1$ and $h=\operatorname{ReLU}(z)$. Then calculate $o=[1,-2]h-0.5$.

## 3 Shapes and capacity

A batch contains seven examples with five features. An MLP has three hidden units and four output classes. Using row-wise scratch notation, state the weight, bias, hidden and logit shapes. Count all trainable parameters. Explain whether ReLU adds parameters.

## 4 Diagnose a repeated-batch loop

Assume `criterion` is ordinary cross-entropy with integer targets, and all tensors and the optimizer are otherwise configured correctly:

```python
for X, y in loader:
    hidden = X @ W1 + b1
    logits = hidden @ W2 + b2
    loss = criterion(torch.softmax(logits, dim=1), y)
    loss.backward()
    optimizer.step()
```

Identify three distinct issues and describe a corrected loop.

## 5 What does the evidence establish?

A hand-constructed network correctly classifies the four XOR corners. A separately trained MLP has 100% training accuracy and 93% held-out accuracy on fresh draws from a synthetic generator.

State what the construction establishes, what the held-out result establishes, and what neither establishes about a physical sensor used by new people.
