# Lecture 7 Concept Check

Ungraded. Show calculations and explain each judgment.

1. Per-example gradients are `[4, 0]`, `[0, 4]`, and `[2, 2]`. Calculate the full-batch mean. What can a one-example stochastic gradient look like?

2. With `v_prev = [2, -1]`, `g = [-1, 3]`, `beta = 0.8`, and `eta = 0.05`, calculate the new momentum velocity and parameter change.

3. Explain why the same learning rate may move too slowly in one direction and oscillate in another on a poorly conditioned loss.

4. Name four controls required for a fair SGD versus Adam comparison.

5. A run reaches low training loss but its validation loss rises. Which optimizer diagnostic and which model-selection action are appropriate?
