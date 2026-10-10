# SE-801 Lecture 5 Nonlinear activations and multilayer perceptrons

Student-facing manuscript. Slides 1–40 form the core route. Slides 41–42 are reserve material. Use the notebook to review the worked calculations and experiment outputs.

---

## Slide 1 Nonlinear activations and MLPs

- SE-801 Artificial Neural Networks
- Lecture 5
- Dr. Muhammad Farrukh Qureshi
- PNEC, NUST
---

## Slide 2 The model family is the next choice

- We already know predictions, losses, gradients and updates.
- A training loop can optimize only within its chosen model family.
- Today we change the representation before changing the training procedure.
---

## Slide 3 Learning outcomes

- Explain the affine boundary and XOR contradiction.
- Trace hidden activations, shapes and parameters.
- Implement the same MLP with tensors and nn.Sequential.
- Use controlled comparisons and validation to assess the result.
---

## Slide 4 A binary affine decision

- s = w₁x₁ + w₂x₂ + b
- Predict class 1 when s ≥ 0.
- The boundary s = 0 is a line in two dimensions.
- What happens to the boundary when we train longer?
---

## Slide 5 Logic targets

- Class labels specify which points must lie together.
- Which columns admit one separating line?

| x₁ | x₂ | AND | OR | XOR |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 | 1 |
| 1 | 0 | 0 | 1 | 1 |
| 1 | 1 | 1 | 1 | 0 |
---

## Slide 6 AND and OR decision boundaries

- AND: s = x₁ + x₂ − 1.5
- OR: s = x₁ + x₂ − 0.5
- Both rules use the same class-1 threshold, s ≥ 0.

**Figure:** AND and OR decision boundaries. The PowerPoint contains an editable data chart generated from the notebook evidence.
---

## Slide 7 XOR places positive points on opposite corners

- Class 1 occupies (0,1) and (1,0).
- Class 0 occupies (0,0) and (1,1).
- Can one half-plane contain exactly the two positive corners?

**Figure:** XOR places positive points on opposite corners. The PowerPoint contains an editable data chart generated from the notebook evidence.
---

## Slide 8 The XOR inequalities contradict each other

- b < 0, w₁ + b ≥ 0, w₂ + b ≥ 0
- The two positive corners imply w₁ + w₂ + 2b ≥ 0.
- Therefore w₁ + w₂ + b ≥ −b > 0.
- But (1,1) needs w₁ + w₂ + b < 0.
---

## Slide 9 A perceptron updates after a mistake

- For labels 0 and 1, let e = y − predicted label.
- On a mistake: w ← w + ηex and b ← b + ηe.
- The boundary family remains affine.
- The convergence guarantee requires linear separability.
---

## Slide 10 Two affine layers

- h = W₁x + b₁
- o = W₂h + b₂
- These equations use column-vector notation.
- What is the complete input-to-logit map?

**Reference:** [Primary reading/documentation](https://d2l.ai/chapter_multilayer-perceptrons/mlp.html)
---

## Slide 11 The effective affine map

- o = (W₂W₁)x + (W₂b₁ + b₂)
- Effective weight: W₂W₁
- Effective bias: W₂b₁ + b₂
- Depth can change optimization or rank constraints without adding nonlinearity.

**Reference:** [Primary reading/documentation](https://d2l.ai/chapter_multilayer-perceptrons/mlp.html)
---

## Slide 12 Hidden features with an activation

- z = W₁x + b₁
- h = φ(z)
- o = W₂h + b₂
- The output is affine in features that can be nonlinear in x.

**Reference:** [Primary reading/documentation](https://d2l.ai/chapter_multilayer-perceptrons/mlp.html)
---

## Slide 13 Sigmoid

- σ(z) = 1 / (1 + exp(−z))
- Outputs lie between 0 and 1.
- Large magnitudes produce saturation.

**Figure:** Sigmoid. The PowerPoint contains an editable data chart generated from the notebook evidence.

**Reference:** [Primary reading/documentation](https://d2l.ai/chapter_multilayer-perceptrons/mlp.html)
---

## Slide 14 Tanh

- tanh(0) = 0
- Outputs lie between −1 and 1.
- Saturation still gives small local derivatives.

**Figure:** Tanh. The PowerPoint contains an editable data chart generated from the notebook evidence.

**Reference:** [Primary reading/documentation](https://d2l.ai/chapter_multilayer-perceptrons/mlp.html)
---

## Slide 15 ReLU

- ReLU(z) = max(0,z)
- Positive inputs retain slope 1.
- Negative inputs become zero.

**Figure:** ReLU. The PowerPoint contains an editable data chart generated from the notebook evidence.

**Reference:** [Primary reading/documentation](https://d2l.ai/chapter_multilayer-perceptrons/mlp.html)
---

## Slide 16 Local activation derivatives

- σ′(z) = σ(z)(1 − σ(z))
- tanh′(z) = 1 − tanh²(z)
- ReLU′(z) is 1 for z > 0 and 0 for z < 0.

**Figure:** Local activation derivatives. The PowerPoint contains an editable data chart generated from the notebook evidence.

**Reference:** [Primary reading/documentation](https://d2l.ai/chapter_multilayer-perceptrons/mlp.html)
---

## Slide 17 ReLU gates an incoming gradient

- z = [−3, 0, 2] gives h = [0, 0, 2].
- Using PyTorch’s zero-at-zero convention, the mask is [0, 0, 1].
- An incoming gradient [2, −1, 4] becomes [0, 0, 4].
- Elementwise multiplication implements this local backward step.
---

## Slide 18 A forward calculation

- x = [1,2]ᵀ
- W₁ has rows [1,−1] and [1,1]. The bias is [0,−1]ᵀ.
- Use ReLU, then output weights [2,−1] and bias 0.5.
- Calculate z, h and the final score before the reveal.
---

## Slide 19 Forward calculation revealed

- The first hidden unit switches off.
- The output score remains a real number.

| Quantity | Value |
| --- | --- |
| z₁ | −1 |
| z₂ | 2 |
| h₁ | 0 |
| h₂ | 2 |
| Output score | −1.5 |
---

## Slide 20 Break

- 20 minutes
- Resume with a constructed nonlinear representation of XOR.
---

## Slide 21 A constructed ReLU representation

- h₁ = ReLU(x₁ − x₂)
- h₂ = ReLU(x₂ − x₁)
- r = h₁ + h₂
- Predict class 1 when r ≥ 0.5.
---

## Slide 22 The constructed hidden coordinates

- The two negative corners map to (0,0).
- The positive corners map to (0,1) and (1,0).
- A line h₁ + h₂ = 0.5 separates these hidden features.

**Figure:** The constructed hidden coordinates. The PowerPoint contains an editable data chart generated from the notebook evidence.
---

## Slide 23 The complete XOR check

- Verify the output on every binary input.
- Representability and successful training are separate claims.

| Input | h₁ | h₂ | r | Prediction |
| --- | --- | --- | --- | --- |
| (0,0) | 0 | 0 | 0 | 0 |
| (0,1) | 0 | 1 | 1 | 1 |
| (1,0) | 1 | 0 | 1 | 1 |
| (1,1) | 0 | 0 | 0 | 0 |
---

## Slide 24 Batch tensor shapes

- Examples occupy rows in the scratch implementation.
- Z = XW₁ + b₁, H = ReLU(Z), O = HW₂ + b₂

| Tensor | Shape |
| --- | --- |
| X | [N,d] |
| W₁, b₁ | [d,h], [h] |
| Z and H | [N,h] |
| W₂, b₂ | [h,C], [C] |
| Output logits O | [N,C] |

**Reference:** [Primary reading/documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.Linear.html)
---

## Slide 25 Parameter count

- P = dh + h + hC + C
- ReLU has no trainable parameters.
- Batch size changes neither weight nor bias count.

| Layer | Weights | Biases | Total |
| --- | --- | --- | --- |
| 2 inputs, 3 hidden | 6 | 3 | 9 |
| 3 hidden, 2 outputs | 6 | 2 | 8 |
| Network | 12 | 5 | 17 |
---

## Slide 26 Scratch forward computation

- hidden = torch.relu(X @ W1 + b1)
- logits = hidden @ W2 + b2
- loss = F.cross_entropy(logits, y)
- Weights are tensors with requires_grad=True.

**Reference:** [Primary reading/documentation](https://d2l.ai/chapter_multilayer-perceptrons/mlp-implementation.html)
---

## Slide 27 The equivalent nn.Sequential model

- model = nn.Sequential(
-     nn.Linear(2, 8),
-     nn.ReLU(),
-     nn.Linear(8, 2),
- )

**Reference:** [Primary reading/documentation](https://d2l.ai/chapter_multilayer-perceptrons/mlp-implementation.html)
---

## Slide 28 Equivalent implementations need matched tensors

- Copy W₁ᵀ and W₂ᵀ into nn.Linear weights.
- Copy both biases directly.
- Compare logits, loss and every parameter gradient.
- Similar accuracy alone cannot prove implementation equivalence.

**Reference:** [Primary reading/documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.Linear.html)
---

## Slide 29 One matched SGD update

- Matched initial loss: 0.696296
- Use the same learning rate and original gradients.
- Maximum post-update logit difference: 0.0e+00
- Clear gradients before the next backward pass.
---

## Slide 30 Synthetic noisy XOR training data

- Four clusters surround the opposite-corner pattern.
- Class 0 has equal-sign centers. Class 1 has opposite-sign centers.
- The Gaussian noise standard deviation is 0.35.

**Figure:** Synthetic noisy XOR training data. The PowerPoint contains an editable data chart generated from the notebook evidence.
---

## Slide 31 A controlled training comparison

- Train / validation / test: 240 / 80 / 80
- Fit scaling on training features only.
- Use 120 epochs, batches of 32 and SGD learning rate 0.1.
- Freeze the width and seed. Select checkpoints by validation cross-entropy.
---

## Slide 32 Training cross-entropy

- All models use the same loss convention.
- The affine stack has the MLP’s parameter count.
- What behavior changes when ReLU is present?

**Figure:** Training cross-entropy. The PowerPoint contains an editable data chart generated from the notebook evidence.
---

## Slide 33 Validation cross-entropy

- Compare independent validation performance.
- Each checkpoint minimizes validation loss.
- A larger parameter count alone does not remove the affine limitation.

**Figure:** Validation cross-entropy. The PowerPoint contains an editable data chart generated from the notebook evidence.
---

## Slide 34 Selected validation checkpoints

- The fixed majority baseline reaches 50% accuracy.
- The results describe this balanced synthetic validation sample.

| Model | Parameters | Epoch | Val CE | Val accuracy |
| --- | --- | --- | --- | --- |
| linear | 6 | 3 | 0.6931 | 51.25% |
| affine stack | 42 | 13 | 0.6930 | 50.00% |
| ReLU MLP | 42 | 120 | 0.0313 | 100.00% |
---

## Slide 35 The learned nonlinear decision regions

- Grid colors show the frozen MLP’s predicted class.
- The plotted region uses original feature coordinates.
- Grid predictions are model outputs, not new observed measurements.

**Figure:** The learned nonlinear decision regions. The PowerPoint contains an editable data chart generated from the notebook evidence.
---

## Slide 36 Frozen held-out test report

- Report both the comparison and its evaluation population.
- This test measures fresh draws from the same synthetic mixture.

| Model | Test CE | Test accuracy | Balanced accuracy |
| --- | --- | --- | --- |
| linear | 0.6944 | 51.25% | 51.25% |
| affine stack | 0.6944 | 52.50% | 52.50% |
| ReLU MLP | 0.0753 | 97.50% | 97.50% |
---

## Slide 37 Representation optimization and generalization

- Representation: can the model express the required relationship?
- Optimization: did training find useful parameters?
- Generalization: does the frozen model work on independent cases?
- Match each proposed intervention to the failure it addresses.
---

## Slide 38 Universal approximation and its limits

- Suitable nonlinear networks can approximate continuous functions on compact domains.
- The statement concerns existence of parameters.
- Training success and generalization still require evidence.
- Width, data and computational constraints matter in practice.

**Reference:** [Primary reading/documentation](https://d2l.ai/chapter_multilayer-perceptrons/mlp.html)
---

## Slide 39 A short training-loop diagnosis

- hidden = X @ W1 + b1
- logits = hidden @ W2 + b2
- loss = criterion(torch.softmax(logits, 1), y)
- loss.backward()
- optimizer.step()

**Reference:** [Primary reading/documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)
---

## Slide 40 Exit questions and project checkpoint

- Explain the affine collapse and XOR limitation.
- Trace a 2-input, 3-hidden, 2-output model and count its parameters.
- State one limitation of the synthetic test result.
- Bring a two-page project proposal with a baseline, split and metric.

**Reference:** [Primary reading/documentation](https://d2l.ai/chapter_multilayer-perceptrons/mlp-implementation.html)
---

## Slide 41 Reserve repeated initializations

- Report every registered seed.
- These repeats share one validation sample.
- Initialization variability differs from population uncertainty.

| Seed | Selected epoch | Validation CE | Validation accuracy |
| --- | --- | --- | --- |
| 31 | 120 | 0.0313 | 100.00% |
| 32 | 113 | 0.0241 | 100.00% |
| 33 | 109 | 0.0240 | 100.00% |
| 34 | 119 | 0.0181 | 100.00% |
| 35 | 109 | 0.0479 | 98.75% |
---

## Slide 42 Reserve an inactive ReLU

- A negative preactivation produces zero local derivative.
- A unit that stays inactive can stop receiving a learning signal.
- ReLU at zero has no mathematical derivative.
- Use the stated implementation convention and avoid the kink in finite differences.
