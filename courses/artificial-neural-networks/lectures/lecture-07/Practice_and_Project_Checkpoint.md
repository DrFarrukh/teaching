## Required project evidence after Lecture 7

- Commit a verified train, validation, and test split.
- Run one baseline with a recorded optimizer, learning rate, batch size, initialization seed, and update budget.
- Save training and validation learning curves.
- Explain one failed or unstable configuration using evidence.
- Do not tune against the test set.

## Practice

1. Re-run the optimizer comparison with one deliberately poor learning rate and diagnose the curve.
2. Repeat the batch-gradient variability measurement with a second parameter state.
3. Add a learning-rate schedule to one optimizer while preserving the original baseline.
