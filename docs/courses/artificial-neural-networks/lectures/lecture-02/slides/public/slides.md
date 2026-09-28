# Linear Regression

Artificial Neural Networks

---

## Today’s learning outcomes

Derive a regression update for a batch.

Build and inspect a complete training loop.

Match the same model with torch.nn.

Explain failed training using evidence.

---

## Retrieval: the second update

𝑥 = [1, 2, 3] 𝑦 = [3, 5, 7]

After step 1: 𝑤 = 34/15, 𝑏 = 1

𝑀𝑆𝐸 = 224/675 ≈ 0.33185



![Figure for slide 3](public/figures/figure-slide-03-01.png)


![Figure for slide 3](public/figures/figure-slide-03-02.png)


![Figure for slide 3](public/figures/figure-slide-03-03.png)


![Figure for slide 3](public/figures/figure-slide-03-04.png)

---

## A calibration problem

Input 𝑥: a sensor reading

Target 𝑦: a reference measurement

Prediction: 𝑦=𝑤𝑥+𝑏



![Figure for slide 4](public/figures/figure-slide-04-01.png)


![Figure for slide 4](public/figures/figure-slide-04-02.png)


![Figure for slide 4](public/figures/figure-slide-04-03.png)


![Figure for slide 4](public/figures/figure-slide-04-04.png)

---

## Regression and an affine neuron

𝑦 = 𝑤1𝑥1 + 𝑤2𝑥2 + … + 𝑤𝑑𝑥𝑑 + 𝑏

The output is a continuous value.

An identity activation leaves the weighted sum unchanged.

The bias allows a nonzero prediction at 𝑥 = 0.


![Figure for slide 5](public/figures/figure-slide-05-01.png)


![Figure for slide 5](public/figures/figure-slide-05-02.png)

---

## Observed data and candidate predictions

Three observations can already distinguish candidate lines.

Which line has the smaller total squared residual?

---

## Squared error and mean squared error

$e_i = \hat{y}_i-y_i = wx_i+b-y_i$

$$L=\frac{1}{N}\sum_{i=1}^{N}e_i^2$$

Squaring prevents sign cancellation.

Averaging makes the scale easier to compare across batches.


![Figure for slide 7](public/figures/figure-slide-07-01.png)


![Figure for slide 7](public/figures/figure-slide-07-02.png)

---

## Why squared error appears in regression

Assume 𝑦 = 𝑓(𝑥) + 𝜀, with independent 𝜀 ~ 𝑁𝑜𝑟𝑚𝑎𝑙(0, 𝜎²).

Negative log-likelihood = 𝑐𝑜𝑛𝑠𝑡𝑎𝑛𝑡 + Σᵢ 𝑒ᵢ² / (2𝜎²)

For fixed σ², minimizing it also minimizes squared error.


![Figure for slide 8](public/figures/figure-slide-08-01.png)


![Figure for slide 8](public/figures/figure-slide-08-02.png)

---

## Derive the gradients

For each observation, let $\hat y_i=wx_i+b$ and $e_i=\hat y_i-y_i$. The mean squared error is

$$L(w,b)=\frac{1}{N}\sum_{i=1}^{N}e_i^2.$$

By the chain rule, $\partial e_i/\partial w=x_i$ and $\partial e_i/\partial b=1$. Therefore

$$\frac{\partial L}{\partial w}=\frac{2}{N}\sum_{i=1}^{N}e_ix_i,\qquad
\frac{\partial L}{\partial b}=\frac{2}{N}\sum_{i=1}^{N}e_i.$$

Gradient descent updates both parameters using the same pre-update gradients:

$$w^+=w-\eta\frac{\partial L}{\partial w},\qquad
b^+=b-\eta\frac{\partial L}{\partial b}.$$

---

## One step, checked numerically

Step

w

b

Full-data MSE

27.666667

2.266667

1.000000

0.331852

2.017778

0.893333

0.005267

---

## Learning rate and the loss trajectory

Same data. Same initial weights.

Only η changes.

---

## Many examples and many features

X: [N, d] w: [d, 1] b: [1]

y: [N, 1] y_hat: [N, 1]

y_hat = X @ w + b

Each row of X is one example.

---

## Two-feature gradient example

X = [[1,0], [0,1], [1,1]]

y = [[3], [-2], [0]]

w = [[0], [0]], b = 0, η = 0.1

Find predictions, MSE, both weight gradients and the bias gradient.

---

## Two-feature exercise: solution

e = [−3, 2, 0]ᵀ MSE = 13/3

∇w L = [−2, 4/3]ᵀ ∂L/∂b = −2/3

w_new = [1/5, −2/15]ᵀ b_new = 1/15

y_hat_new = [4/15, −1/15, 2/15]ᵀ

MSE_new = 842/225 ≈ 3.74222

---

## Vectorized gradient and its shapes

E = Xw + b − y [N,1]

∇w L = (2/N) XᵀE [d,1]

∂L/∂b = (2/N) Σᵢ Eᵢ [1]

Every parameter gradient has the parameter’s shape.

---

## Generating data with known weights

y = 2x₁ − 3.4x₂ + 4.2 + ε

ε ~ Normal(0, 0.1²)

1,000 training rows · 140 validation rows · 140 test rows

Can training recover approximately the generating coefficients?

---

## Batch, minibatch and stochastic updates

Method

Examples per update

Updates per epoch, N=1000

Full batch

Minibatch

32 (last: 8)

Single-example SGD

---

## Epochs are not update steps

N = 1,000, batch size = 32

31 complete batches + one batch of 8

32 updates per epoch

20 epochs → 640 updates

What changes if the batch size becomes 100?

---

## The complete training algorithm

Initialize the parameters once.

For each epoch: shuffle the training indices.

For each batch: predict → loss → backward → update → clear gradients.

After the epoch: measure loss using the current model.

---

## Implementation map

Data iterator → minibatches

Parameters → tensors requiring gradients

Model → X @ w + b

Loss → mean squared residual

SGD → a parameter update under no_grad

---

## A data iterator from scratch

indices = torch.randperm(len(X), generator=g)

for start in range(0, len(X), batch_size):

selected = indices[start:start + batch_size]

yield X[selected], y[selected]

Trace each line using one batch before running the full loop.

---

## Model, loss and parameters

w = initial_w.clone().requires_grad_()

b = initial_b.clone().requires_grad_()

prediction = X_batch @ w + b

assert prediction.shape == y_batch.shape

loss = ((prediction - y_batch)**2).mean()

Trace each line using one batch before running the full loop.

---

## The manual SGD update

loss.backward()

with torch.no_grad():

for parameter in [w, b]:

parameter -= learning_rate * parameter.grad

parameter.grad.zero_()

Trace each line using one batch before running the full loop.

---

## The outer training loop

for epoch in range(epochs):

for xb, yb in data_iter(batch_size, X, y, g):

loss = mse(linear_model(xb, w, b), yb)

loss.backward()

sgd([w, b], learning_rate)

# Evaluate the updated model after the epoch.

Trace each line using one batch before running the full loop.

---

## Training curves and parameter recovery

Compare learned weights with [2, −3.4].

Compare learned bias with 4.2.

Loss near the noise variance is plausible.

Exact recovery is not expected from a finite noisy sample.

---

## Checkpoint: rebuild the loop in words

A batch enters the model. What happens next?

Name one shape check.

Name one gradient-management rule.

Name one useful diagnostic beyond a printed loss.

---

## The same mathematics in torch.nn

Scratch

PyTorch equivalent

X @ w + b

nn.Linear(2, 1)

((prediction − y)**2).mean()

nn.MSELoss()

parameter -= η * parameter.grad

torch.optim.SGD

clear .grad

optimizer.zero_grad()

manual iterator

TensorDataset + DataLoader

---

## The framework training step

optimizer.zero_grad()

prediction = model(xb)

loss = criterion(prediction, yb)

loss.backward()

optimizer.step()

Trace each line using one batch before running the full loop.

---

## Weight orientation and multiple outputs

Scratch: w has shape [d, 1]

nn.Linear: weight has shape [out_features, in_features]

For nn.Linear(2, 3):

X [B,2] @ weight.T [2,3] + bias [3] → output [B,3]

---

## Verify equivalence fairly

Match the data and batch order.

Copy the same initial parameters.

Use the same loss reduction, learning rate and update budget.

Compare predictions, not just the final printed loss.

---

## Experiment: batch size

Keep the learning rate and epoch count fixed.

Compare batches of 1, 32 and 1,000.

Does equal epoch count mean equal update count?

---

## Debugging: a silent broadcasting error

prediction.shape = [3, 1]

target.shape = [3]

(prediction - target).shape = ?

Prediction and target values are both 3, 5, 7.

Will this code report zero loss?

---

## Debugging: three training mistakes

A. Initialize w inside every epoch.

B. Call backward() repeatedly without clearing .grad.

C. Take mean loss, then divide gradients by batch size again.

For each: explain the effect and repair the code.

---

## An independent least-squares reference

A = [X | 1] θ = [w; b]

Solve minθ ||Aθ − y||²

reference = torch.linalg.lstsq(A, y).solution

Use the training data for this reference.

---

## Prediction accuracy and identifiable weights

Suppose feature 2 duplicates feature 1.

y_hat = w₁x + w₂x = (w₁+w₂)x

[2,3] and [1,4] produce the same predictions.

The data can identify the sum, but not both weights separately.

---

## Held-out evaluation and a baseline

Fix the model choices before reading test results.

Compare with a constant prediction: training-target mean.

Report MSE and RMSE.

RMSE has the same units as the target.

---

## Lecture 2 synthesis

A training loop repeatedly changes shared parameters.

Correct shapes and loss scaling are part of the mathematics.

Scratch and framework implementations should agree under matched conditions.

---

## Reserve: noise and achievable error

For y = f(x) + ε and E[ε]=0:

E[(f(x) − y)²] = Var(ε)

Predict the MSE when noise standard deviation doubles.

---

## Reserve: feature scaling and stability

Replace x by 100x and adjust the true slope accordingly.

The prediction family can stay the same.

The gradient magnitudes and curvature change.

Should the same learning rate still work?

---

## Reserve: gradient verification

Analytical derivative

Autograd derivative

Central finite difference:

[L(w+h) − L(w−h)] / (2h)

Why can an extremely small h be unreliable?
