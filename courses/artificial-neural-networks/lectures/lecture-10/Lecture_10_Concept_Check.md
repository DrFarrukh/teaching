# Lecture 10 Concept Check

Show all shape and parameter calculations.

1. Why does parameter sharing reduce the number of learned values compared with a dense layer?

2. An input has shape `[8,3,32,32]`. What is the output shape of `Conv2d(3,16,kernel_size=3,padding=1,stride=1)`?

3. How many trainable parameters does that layer contain when bias is enabled?

4. Find the output size for an input width of `28`, kernel size `5`, padding `2`, stride `2`, and dilation `1`.

5. Apply 2 × 2 max pooling with stride 2 to:

```text
1 3 2 0
4 6 5 1
0 2 7 8
1 3 4 9
```

6. Distinguish translation equivariance from translation invariance in one sentence each.

7. A classifier obtains 100% validation accuracy when all training and validation objects are centrally located. What split would test whether the model transfers across spatial position?

8. Why can a model with perfect validation accuracy still fail at deployment?
