## Required project evidence after Lecture 9

- Refactor the baseline into `nn.Module`, data, training, and evaluation components.
- Store the resolved configuration with each run.
- Save the best validation checkpoint and reload it in a fresh process.
- Verify prediction equivalence on a frozen batch.
- Record parameter count, checkpoint size, software versions, and device.

## Practice

1. Remove optimizer state from a resume checkpoint and quantify the divergence.
2. Add a persistent buffer and confirm that it follows device moves and serialization.
3. Test a loader with multiple workers only after the single-worker reference passes.
