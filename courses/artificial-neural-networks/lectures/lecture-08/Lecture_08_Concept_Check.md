# Lecture 8 Concept Check

Ungraded. Show calculations and explain each judgment.

1. For `X:[8,4]`, `W1:[4,12]`, `b1:[12]`, `W2:[12,3]`, and `b2:[3]`, give the shapes of the hidden activation and logits.

2. Why must `CrossEntropyLoss` receive logits rather than probabilities produced by an external softmax?

3. A scratch model and an `nn.Module` produce identical logits. What additional test checks their backward implementations?

4. Explain why `[B,1] - [B]` creates the wrong regression loss. Give one repair.

5. A team repeatedly checks the test score while tuning. What scientific contract did it break, and what should it do next?
