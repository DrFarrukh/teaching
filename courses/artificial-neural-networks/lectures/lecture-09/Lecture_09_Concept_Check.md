# Lecture 9 Concept Check

Ungraded. Show calculations and explain each judgment.

1. A tensor attribute has `requires_grad=True` but does not appear in `named_parameters()`. What likely happened, and how should the tensor be registered?

2. List the minimum contents of an inference artifact and the additional state needed to resume Adam training.

3. Why can two DataLoaders with the same seed still produce different future orders after one has already completed an epoch?

4. Write the test that verifies a reloaded model preserves predictions.

5. Why does exact CPU resume in the lecture notebook not guarantee bitwise equality across different GPU models and software versions?
