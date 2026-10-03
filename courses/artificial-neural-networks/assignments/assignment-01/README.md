# SE-801 Artificial Neural Networks

## Individual Assignment 1: Can a Linear Classifier Diagnose a Synthetic Sensor?

| Item | Details |
|---|---|
| Coverage | Lectures 1–4: tensors, autograd, linear models, generalization, regularization, softmax and cross-entropy |
| Due | **Thursday 8 October 2026, 23:59 Pakistan time** |
| Mode | Individual take-home assignment |
| Maximum marks | 20 |
| Submit | `SE801_A1_<StudentID>.pdf` and `SE801_A1_<StudentID>.zip` |
| Tools | Python, PyTorch, NumPy, Matplotlib; CPU only |
| Starter | [SE801_A1_Starter](SE801_A1_Starter/) — data generator, report outline and notebook scaffold; no training solution |

## The question

A synthetic sensor has three labelled states: normal, offset and unstable. Its two measurements overlap, so even a correctly trained classifier will make mistakes. A colleague reports high accuracy and concludes that the model is ready for use on real machinery.

**Build and evaluate a linear classifier, then decide which part of that claim your experiment supports.** The labels describe simulated states; they are not real fault diagnoses. Marks reward correct reasoning and controlled evidence, not the highest accuracy.

## Data and experimental rules

Run the supplied `generate_data.py` once. It creates fixed training, validation and test CSV files using seed 801. Each has two numeric features, `reading_1` and `reading_2`, a unique `sample_id`, and a class index `label` in `{0,1,2}`. Training has 600/200/100 examples by class; validation and test each have 180/60/30. Do not change the generator, rebalance the evaluation splits, or create replacement splits.

- Use only the two readings as features. IDs and labels are not predictors.
- Fit feature means and population standard deviations on training data only. Apply them unchanged to validation and test.
- Set and report seeds. Train on CPU with minibatch SGD, batch size 64, learning rate 0.05, no momentum, and 100 epochs. Shuffle training examples only.
- Compare `lambda` in `{0, 0.01, 0.1}`. Use identical initialization and minibatch order across candidates. Do not use class weights, oversampling or a nonlinear network.
- Use mean cross-entropy and the objective `J = mean_CE + (lambda/2) * sum(W**2)`. Penalize weights only, once. Bias is not penalized. Explicit loss regularization with optimizer weight decay zero is the simplest route.
- Record unpenalized training and validation cross-entropy every epoch. Select a candidate and epoch by lowest validation cross-entropy; break ties by smaller lambda, then earlier epoch. Restore that checkpoint.
- Keep test data out of all decisions. After freezing the recipe, evaluate the selected model and the required baseline on test data in one final evaluation stage.

## Part A — Shapes, stable loss and gradient evidence [4 marks]

Use this single example in `torch.float64`:

```python
x = torch.tensor([[1.5, -0.5]], dtype=torch.float64)
W = torch.tensor([[0.2, -0.1, 0.3],
                  [0.4,  0.2, -0.2]], dtype=torch.float64)
b = torch.tensor([0.1, -0.2, 0.0], dtype=torch.float64)
y = torch.tensor([2], dtype=torch.long)
logits = x @ W + b
```

1. State the shapes of a batch `X`, scratch weights `W`, bias, logits and class-index targets for this problem. Explain the different stored weight shape in `nn.Linear(2, 3)`.
2. Calculate probabilities and loss using `log_softmax` or `logsumexp`. Add 1,000 to all three logits and demonstrate unchanged probabilities/loss with the stable calculation. Explain why a direct exponential calculation can fail.
3. Derive `d(loss)/d(logits) = p - one_hot(y)`, then calculate the weight and bias gradients for this example. Compare your values with autograd in a table. Explain why `nn.CrossEntropyLoss` receives raw logits and integer class indices.

## Part B — Build and verify the model [5 marks]

1. Audit the generated splits: row counts, class counts, duplicate IDs, feature types and missing values. Show that IDs do not overlap. Save the train-only scaling parameters. [1]
2. Implement the scratch model with trainable leaf tensors, `X @ W + b`, stable log probabilities, class-index selection and a mean loss. Implement minibatches and SGD updates using tensor operations and autograd. Do not use `nn.Linear`, `nn.CrossEntropyLoss` or a PyTorch optimizer for this implementation. Update under `torch.no_grad()` and clear gradients. Train the lambda-zero model. [2]
3. Implement the equivalent `nn.Linear` model with `nn.CrossEntropyLoss` and `torch.optim.SGD`. Copy the scratch model's initial parameters, transpose weights correctly, and verify logits and unregularized loss agree on the same batch before training. Train with the same seed, batch order and settings. Report the maximum absolute differences in initial logits/loss and compare final validation losses. Small floating-point differences are acceptable; diagnose substantial disagreement. [2]

## Part C — Generalization and model selection [5 marks]

Using either implementation, run the three required regularization candidates. For each, save its best-validation checkpoint and report lambda, chosen epoch, training CE and validation CE at that epoch, and weight norm. Show unpenalized training/validation curves. Explain how fitting error, validation error and weight size change, without assuming regularization must improve performance. [3]

Name the selected model and justify the choice using validation evidence. Explain why test-based selection, fitting the scaler on all splits, or applying the penalty twice would invalidate the experiment. [2]

## Part D — Final evaluation and decision [4 marks]

For the frozen model report test cross-entropy, accuracy, per-class precision/recall/F1, balanced accuracy and macro F1. Use a confusion matrix with rows=true and columns=predicted, labelled with all three class names. Define undefined precision or F1 as zero and disclose that convention. [2]

Compare classification metrics against an always-normal baseline. Do not calculate cross-entropy for its hard predictions. Identify which errors accuracy hides, discuss class imbalance, and write a verdict: useful for this simulation, useful with caveats, or not useful. Specify one real-world claim you refuse to make and what evidence would be needed to make it. Do not interpret softmax probabilities as demonstrated calibration. [2]

## Part E — Reproducibility [2 marks]

The ZIP must contain a notebook or script that regenerates the data, runs every required calculation offline, and saves the tables and figures; the generator; CSV files; a README; and package requirements. Use relative paths and preserve saved notebook outputs. Include a source/AI assistance statement explaining what you checked yourself. No GPU, account or external download is required.

## Report and submission

Follow the portal's report-first format: **at most five A4 pages for the main report**, 11 pt font, margins at least 2 cm. Code and detailed calculations belong in annexes with no page limit. Use these sections:

1. Introduction — sensor story and the question.
2. Problem — predictions, class meanings and what a useful result would establish.
3. Method — data audit, gradient verification, scaling, implementations and fixed protocol.
4. Results — verification table, candidate table, confusion matrix, metrics and **at most three numbered figures** (panels allowed).
5. Discussion — verdict, error tradeoffs, limits and the refused claim.

Annex A: complete readable code. Annex B: worked gradients, data dictionary and configuration. Annex C: sources and assistance statement. Submit the PDF and ZIP separately; keep the ZIP below 10 MB. Every numerical claim must be traceable to your saved results. This assignment's 20 marks do not announce or alter course assessment weights.

## Marking rubric

| Criterion | Marks | Evidence |
|---|---:|---|
| Shapes, stable loss and gradients | 4 | Correct dimensions, stable shift experiment, derivation and autograd agreement |
| Model construction and verification | 5 | Split audit, train-only scaling, correct scratch and concise models, initial equivalence |
| Controlled generalization experiment | 5 | Three comparable runs, saved checkpoints, validation-based choice and interpretation |
| Final evaluation and decision | 4 | Correct class metrics, baseline, supported verdict and real-world boundary |
| Reproducibility | 2 | Offline execution, complete files, readable report and assistance disclosure |
| **Total** | **20** | |

## Common mistakes

- Using MSE on arbitrary class codes, or applying softmax before `CrossEntropyLoss`.
- Mixing scratch `[2,3]` weights with `nn.Linear` `[3,2]` weights without transposing.
- Accumulating gradients, retaining a checkpoint that continues to mutate, or reporting penalized loss as CE.
- Choosing settings from test scores or claiming accuracy alone proves minority-class performance.
- Treating synthetic labels as evidence of real sensor faults.

## Suggested timeline and checklist

By 4 October: generate/audit data and complete the worked example. By 5–6 October: verify both implementations and run candidates. On 7 October: freeze the model, evaluate once, write and rerun the report. Submit by **8 October, 23:59 Pakistan time**. Late submissions follow the instructor's announced course policy.

- [ ] Gradients and stable-loss evidence are included.
- [ ] Scaling uses training data only and candidate runs are controlled.
- [ ] The chosen checkpoint is restored before final evaluation.
- [ ] Test metrics and the always-normal baseline are included.
- [ ] PDF main report meets the five-page limit; code is in Annex A.
- [ ] ZIP runs offline from a clean start and assistance is declared.

This is individual work. Discussion of ideas is permitted; submitted code, calculations, figures and prose must be your own and explainable by you. Lectures 1–4 and their notebooks are the primary study references.
