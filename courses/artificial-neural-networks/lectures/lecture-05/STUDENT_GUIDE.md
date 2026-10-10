# SE-801 Lecture 5 Study Guide

This package accompanies the lecture on nonlinear activations and multilayer perceptrons. All example observations are synthetic.

## Study route

1. Read the slides through the XOR limitation. Explain why one affine boundary cannot separate the four XOR corners.
2. Work through affine composition, activation functions and the forward calculation by hand before looking at the worked result.
3. Open `notebook.ipynb` to review the recorded experiment outputs. Use `notebook_live.ipynb` to predict outputs and run each cell yourself, in order.
4. Compare the scratch and `nn.Sequential` implementations, including tensor orientations and the gradient checks.
5. Explain the train/validation/test protocol and distinguish representation, optimization and generalization.
6. Complete `Lecture_05_Concept_Check.md`, then attempt the practice extensions in `Practice_and_Project_Checkpoint.md`.

The notebooks contain every implementation cell. You need no helper module, external dataset, scikit-learn package or GPU. The reserve experiments are optional extensions.

## Running the notebook

Open the notebook in Jupyter or upload it to Google Colab. A local Python environment needs these packages:

```bash
python -m pip install -r requirements.txt
```

Choose a Python kernel in which those packages are installed. Restart the kernel before **Run All**. Run cells in order because later cells use objects created earlier. Generated figures, CSVs and result JSON go into `lecture_05_outputs` in your working directory.

The recorded outputs use deterministic CPU calculations in float64. Other library versions can produce small numerical differences. Use the consistency assertions and the experimental protocol when interpreting a rerun.

## Reading the evidence

The nonlinear network represents the XOR rule. Its held-out performance describes new samples from the same synthetic mixture. Neither result establishes performance on a real sensor or new people.

Fit preprocessing on the training split. Select checkpoints using validation loss. Keep the test split outside model selection. If you change the recipe after examining its test results, use new independent evaluation data for a new test claim.

The concept check and practice tasks are ungraded unless the instructor announces otherwise. The project checkpoint is a proposal brief; its marks and submission date come from the instructor.

## Reading

- [D2L 5.1: Multilayer perceptrons](https://d2l.ai/chapter_multilayer-perceptrons/mlp.html)
- [D2L 5.2: MLP implementation](https://d2l.ai/chapter_multilayer-perceptrons/mlp-implementation.html)
- [PyTorch Linear](https://docs.pytorch.org/docs/stable/generated/torch.nn.Linear.html)

Lecture 6 develops multilayer backpropagation and stable training.
