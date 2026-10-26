# SE-801 Lecture 8: Feedback and Learning-System Consolidation
## 1. Feedback and learning-system consolidation
- A complete chain from data to reproducible evidence

## 2. Learning outcomes
- Trace shapes and responsibilities through an MLP pipeline
- Connect logits, cross-entropy, gradients, and parameter updates
- Verify a scratch implementation against nn.Module
- Detect leakage, broadcasting errors, and invalid metric claims
- Write a reproducible experiment record for a project baseline

## 3. Diagnostic themes from Lectures 1 to 7
- Tensor shapes carry meaning and can fail silently through broadcasting
- The loss contract determines what logits and labels mean
- Representation limits differ from optimization problems
- Evaluation must remain independent of model selection

## 4. The complete learning system
- question
- split
- preprocessing
- model
- loss
- gradient
- update
- validation
- test report

## 5. Case file: a compact three-class problem
| Object | Shape |
|---|---|
| X batch | [B, 4] |
| y batch | [B] |
| W1 | [4, 12] |
| b1 | [12] |
| W2 | [12, 3] |
| b2 | [3] |

- Input: four measured features per example
- Target: one of three class indices
- Training, validation, and test sets are generated independently
- Train-only mean and scale transform every split

## 6. Student trace: forward shapes
- For B = 5, write the shapes of Z1, H, and logits
- State which dimension indexes examples
- State which dimension CrossEntropyLoss interprets as classes
- Explain why softmax is absent from the model's forward method

## 7. Forward-shape answer
- Z1 and H have shape [5, 12]
- Logits have shape [5, 3]
- Dimension 0 indexes examples and dimension 1 indexes classes
- CrossEntropyLoss consumes raw logits and applies the stable normalization internally

## 8. One MLP, two implementations
- Scratch tensors make every matrix and parameter explicit
- nn.Module registers the same parameters and composes reusable layers
- Equivalence requires identical values, shapes, operations, and reduction
- Matching class names or layer counts is not enough

## 9. Scratch forward pass
```python
z1 = X @ W1 + b1
h = torch.relu(z1)
logits = h @ W2 + b2
loss = F.cross_entropy(logits, y)
```

## 10. Module forward pass
```python
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(4, 12)
        self.fc2 = nn.Linear(12, 3)
    def forward(self, x):
        return self.fc2(torch.relu(self.fc1(x)))
```

**Source:** https://docs.pytorch.org/docs/stable/generated/torch.nn.Module.html

## 11. Parameter orientation must be reconciled
- The scratch expression stores W1 as [input, hidden]
- nn.Linear stores weight as [output, input]
- Copy W1.T into fc1.weight and W2.T into fc2.weight
- Bias vectors already use the same orientation

## 12. Equivalence test before training
- Copy all four parameter tensors
- Run both models on the same batch
- Compare logits and scalar loss
- Backpropagate once and compare every gradient after accounting for transpose

## 13. Reference equivalence evidence

## 14. The training step contract
- Clear stored gradients
- Calculate logits and the scalar loss
- Run reverse-mode differentiation
- Update every parameter using gradients from the same parameter state
- Record the loss before starting the next step

## 15. Student repair: training loop
```python
for X, y in loader:
    probabilities = model(X).softmax(dim=1)
    loss = criterion(probabilities, y)
    loss.backward()
    optimizer.step()
```
- Identify two faults
- Write the corrected order
- Explain the consequence of each fault

## 16. Training-loop repair
- Pass raw logits to CrossEntropyLoss
- Clear gradients before the new backward pass
- Use forward and loss, backward, then optimizer.step()
- Apply softmax only when probabilities are needed for interpretation

## 17. Broadcasting can create the wrong problem
- Predictions shaped [B, 1] and targets shaped [B] produce [B, B] differences
- Every prediction becomes paired with every target
- The code runs and returns a scalar, so shape assertions matter
- Align both tensors as [B] or both as [B, 1]

## 18. Student calculation: the false zero-loss case
- pred = [[1], [2], [3]] and target = [1, 2, 3]
- Write the broadcast difference matrix
- Calculate the mean squared error reported by the faulty code
- State the correct MSE after matching shapes

## 19. Broadcasting answer
- The 3 by 3 matrix has rows [0,-1,-2], [1,0,-1], [2,1,0]
- Squared values sum to 12, so the faulty mean is 12/9
- Matched shapes compare only the diagonal pairs
- The correct MSE is zero

## 20. Break
- 20 minutes
- After the break: evaluation contracts, evidence, and project repair

## 21. Representation or optimization?
- A linear model failing on XOR has insufficient representation
- A capable MLP stuck at chance may have an optimization or implementation fault
- A lower learning rate cannot add a nonlinear feature
- A larger model cannot repair labels that leak across splits

## 22. Training, validation, and test responsibilities
| Split | Permitted use |
|---|---|
| Training | Fit parameters and training-only preprocessing |
| Validation | Choose architecture, hyperparameters, and checkpoint |
| Test | Evaluate the frozen pipeline once for the final claim |


## 23. Student judgment: which result can be claimed?
- Model A has 99% training accuracy and 62% validation accuracy
- Model B has 88% training accuracy and 84% validation accuracy
- The test set has not been opened
- Choose the next action and explain what cannot yet be claimed

## 24. Evaluation answer
- Model B currently has stronger validation evidence
- Neither model has a final test estimate
- The choice should use the declared validation metric and protocol
- A training score does not estimate generalization

## 25. Accuracy can hide the class that matters
- Always-normal prediction can achieve 80% accuracy in an 80 to 20 split
- Fault recall then equals zero
- Balanced accuracy exposes unequal class recall
- Metric selection must follow the operational question

## 26. Controlled end-to-end experiment
| Evidence | Purpose |
|---|---|
| Max logit error | Forward equivalence |
| Max gradient error | Backward equivalence |
| Learning curves | Optimization diagnosis |
| Confusion matrix | Class-specific test behavior |

- Synthetic three-class data with four input features
- Train-only standardization
- Scratch and module forward and gradient equivalence
- Module training with validation checkpoint selection
- Frozen test evaluation after the recipe is fixed

## 27. Learning curves for the consolidated system
- Training loss shows parameter fit
- Validation loss controls checkpoint selection
- A widening gap signals overfitting under this protocol
- Curves cannot detect every form of leakage

## 28. Reference-run evidence

## 29. Reproducibility record
- Question and prediction
- Data origin, split identifiers, and preprocessing fit set
- Model definition and parameter count
- Loss, optimizer, learning rate, batch size, and budget
- Seeds, selected checkpoint rule, metrics, and software versions

## 30. One seed answers a narrow question
- A fixed seed makes one run repeatable under its environment
- It does not measure sensitivity to initialization or data sampling
- Repeated runs estimate variation under specified sources of randomness
- A reproducible mistake remains a mistake

## 31. Project clinic: scope and baseline
- Write one falsifiable project question
- Choose a baseline that addresses the same target and split
- State the intended unit of generalization such as subject, session, or device
- Remove any feature unavailable at deployment time

## 32. Project clinic: evidence table
| Claim | Required evidence |
|---|---|
| Improves the baseline | Same split, metric, and selection budget |
| Works for new subjects | Subject-disjoint held-out evaluation |
| Training is stable | Curves, gradient checks, and repeated runs |
| Fits the device | Measured size, memory, and latency |


## 33. Notebook investigation
```python
python lecture_08_experiments.py
# or open ANN_Lec_8_live.ipynb
```
- Verify scratch and nn.Module logits
- Compare all four parameter gradients
- Train the frozen module recipe
- Inspect learning curves and the test confusion matrix
- Trigger the broadcasting fault and verify the shape assertion

## 34. Concept check
- Why are raw logits required by CrossEntropyLoss?
- What does a forward-equivalence test fail to verify?
- Why does validation choose a checkpoint while test does not?
- How can a model be reproducible but scientifically invalid?

## 35. Lecture synthesis
- Shapes connect the mathematics to the code
- The loss and training-loop contracts determine valid gradients
- Equivalence tests isolate implementation faults
- Split discipline and experiment records support believable evidence

## 36. Reserve: finite-difference gradient check
- Perturb one scalar parameter by plus and minus epsilon
- Compare the centered finite difference with autograd
- Use double precision and several epsilon values
- Treat agreement as a local implementation check

## 37. Reserve: ablation logic
- Remove or change one component while preserving the rest of the protocol
- State the mechanism the ablation tests
- Report uncertainty rather than selecting only a favorable run
