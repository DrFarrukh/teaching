# SE-801 Lecture 9: PyTorch Engineering and Reproducible Experiments
## 1. PyTorch engineering and reproducible experiments
- Turning a correct notebook into maintainable research code

**Source:** https://en.d2l.ai/chapter_builders-guide/

## 2. Learning outcomes
- Build custom and nested nn.Module components
- Inspect registered parameters, buffers, and state-dict keys
- Create reproducible dataset and DataLoader pipelines
- Write device-independent training and evaluation loops
- Save, reload, and resume a training run with verified equivalence

## 3. Engineering preserves the scientific contract
- The refactor must preserve the model function and data split
- Reusable components make assumptions visible
- Checkpoints preserve state across interruptions
- Verification tests detect accidental changes

## 4. What nn.Module owns
| State type | Example | In state_dict |
|---|---|---|
| Parameter | Linear weight | Yes |
| Persistent buffer | running statistic | Yes |
| Ordinary tensor attribute | temporary cache | No |

- Submodules assigned as attributes become part of the module tree
- nn.Parameter objects become trainable registered parameters
- Persistent buffers store non-trainable tensor state
- train() and eval() propagate mode changes through descendants

**Source:** https://docs.pytorch.org/docs/stable/generated/torch.nn.Module.html

## 5. Custom module contract
```python
class ResearchMLP(nn.Module):
    def __init__(self, in_features, hidden, classes):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(in_features, hidden), nn.ReLU())
        self.head = nn.Linear(hidden, classes)
    def forward(self, x):
        return self.head(self.encoder(x))
```

## 6. Student trace: registered names
- List the parameter names produced by named_parameters()
- Give the shape of each tensor for in_features=4, hidden=16, classes=3
- Calculate the total trainable parameter count

## 7. Registered-name answer
- encoder.0.weight [16,4] and encoder.0.bias [16]
- head.weight [3,16] and head.bias [3]
- Total = 16x4 + 16 + 3x16 + 3 = 131
- ReLU owns no trainable parameters

## 8. Sequential and custom composition
- nn.Sequential fits a straight chain of modules
- A custom forward method supports branching, reuse, and shape checks
- Named submodules improve inspection and checkpoint diagnostics
- Choose the simplest structure that expresses the actual computation

## 9. Residual-style block
```python
class ResidualMLPBlock(nn.Module):
    def __init__(self, width):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(width, width), nn.ReLU(),
            nn.Linear(width, width))
    def forward(self, x):
        return torch.relu(x + self.net(x))
```

## 10. Shape compatibility in a residual addition
- The main path and skip path must produce the same shape
- A projection can reconcile different widths
- Broadcasting is usually the wrong repair for feature dimensions
- Assert the intended shape before the addition

## 11. Parameter initialization after construction
```python
def init_linear(module):
    if isinstance(module, nn.Linear):
        nn.init.kaiming_uniform_(module.weight, nonlinearity='relu')
        nn.init.zeros_(module.bias)
model.apply(init_linear)
```
- Use module.apply() to visit nested layers
- Match the rule to the activation when the experiment requires it
- Record the initialization and its seed
- Verify a representative weight distribution rather than assuming the hook ran

## 12. Dataset separates storage from sampling
- Dataset defines how one indexed example is retrieved
- DataLoader defines batching and sampling order
- A split must be created before loaders are constructed
- Preprocessing statistics must come from the training split

**Source:** https://docs.pytorch.org/docs/stable/data.html

## 13. A reproducible DataLoader
```python
generator = torch.Generator().manual_seed(20261102)
loader = DataLoader(
    train_set, batch_size=64, shuffle=True,
    generator=generator, num_workers=0)

```
- The generator controls the random sampler in this reference setup.

**Source:** https://docs.pytorch.org/docs/stable/data.html

## 14. Student judgment: two loaders
- Loader A and Loader B receive generators with the same seed
- Both use the same dataset, batch size, and shuffle=True
- Predict whether the first epoch index order matches
- Predict what happens if one generator has already produced an epoch

## 15. Loader-order answer
- Fresh generators with identical state produce the same first permutation
- Advancing one generator changes its later permutations
- A seed value alone is insufficient when resuming mid-run
- Saving generator state preserves the continuation point

## 16. Worker randomness needs its own plan
- The main process chooses map-style sample indices
- Each worker receives a PyTorch seed derived from the loader seed
- Other libraries used inside workers may require explicit seeding
- Keep the classroom reference at num_workers=0 before adding concurrency

**Source:** https://docs.pytorch.org/docs/stable/data.html

## 17. Device-independent ownership
```python
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
for X, y in loader:
    X = X.to(device)
    y = y.to(device)
    logits = model(X)
```

## 18. Device errors reveal split ownership
- The model and every tensor used in an operation must share a device
- Create temporary tensors from existing tensors when possible
- Load checkpoints with an explicit map_location
- Measure memory and latency on the deployment device, not only the development machine

## 19. Break
- 20 minutes
- After the break: checkpoints, exact resume, and experiment records

## 20. state_dict names the model state
| Example key | Meaning |
|---|---|
| encoder.0.weight | First linear-layer weights |
| block.net.2.bias | Second linear layer in the residual block |
| head.weight | Classifier weights |

- Keys follow the nested module path
- Values include registered parameters and persistent buffers
- The architecture must be reconstructed before loading weights
- Strict loading exposes missing or unexpected keys

**Source:** https://docs.pytorch.org/docs/stable/generated/torch.nn.Module.html

## 21. Inference save and reload
```python
torch.save(model.state_dict(), path)
reloaded = ResearchMLP(...).to(device)
state = torch.load(path, map_location=device, weights_only=True)
reloaded.load_state_dict(state, strict=True)
reloaded.eval()
```

**Source:** https://docs.pytorch.org/tutorials/beginner/saving_loading_models

## 22. Prediction-equivalence test
- Set both models to evaluation mode
- Use the same frozen input batch
- Compare logits with a declared numerical tolerance
- A matching file size or load message is not a prediction test

## 23. A training checkpoint needs more state
| Checkpoint item | Why it matters |
|---|---|
| model_state_dict | Learned parameters and buffers |
| optimizer_state_dict | Momentum or adaptive moments |
| epoch and best metric | Continuation and selection |
| random-generator states | Future dropout and shuffle sequence |
| configuration | Reconstruct the intended run |


**Source:** https://docs.pytorch.org/tutorials/beginner/saving_loading_models

## 24. Student repair: incomplete checkpoint
```python
torch.save({
    'epoch': epoch,
    'model': model.state_dict(),
}, path)
```
- The run uses Adam and shuffled minibatches
- List the missing state required for a faithful resume
- Separate state needed for inference from state needed for continuation

## 25. Checkpoint repair
- Inference needs the architecture, model state, preprocessing, and label mapping
- Resume also needs optimizer state and the next epoch or step
- Exact continuation requires relevant random-generator states
- The configuration and software environment make the result interpretable

## 26. Checkpoint loading order
- Construct the model with the recorded configuration
- Construct the optimizer over that model's parameters
- Load the model state and then the optimizer state
- Restore generator states before creating the next shuffled iterator
- Select train or eval mode for the next operation

## 27. Exact-resume reference experiment
| Control | Setting |
|---|---|
| Device | CPU reference |
| Workers | 0 |
| Optimizer | Adam |
| Stochastic layer | Dropout |
| Comparison | Final logits |

- Reference A trains for ten uninterrupted epochs
- Reference B saves after epoch five and reloads into new objects
- The checkpoint restores model, optimizer, loader generator, and CPU RNG state
- Both branches then process the same future minibatches and dropout masks

## 28. Uninterrupted and resumed curves
- The curves should overlap after the resume point
- A mismatch localizes missing or reordered state
- Exact CPU equality is a reference test, not a cross-hardware guarantee

## 29. Reference-run verification

## 30. Checkpoint files are data inputs
- Load only files from trusted sources
- Prefer state dictionaries over pickled model objects
- Use weights_only=True when the saved object is compatible
- Record a hash when a specific artifact supports a reported result

**Source:** https://docs.pytorch.org/docs/stable/generated/torch.load.html

## 31. Configuration before execution
```python
config = {
    'seed': 20261102, 'hidden': 24,
    'batch_size': 64, 'lr': 0.01,
    'epochs': 10, 'split_version': 'synthetic-v1'
}

```
- Save the resolved values, not only command-line defaults.

## 32. Experiment record
- Run identifier and timestamp
- Code revision, environment, and device
- Data and split identifiers
- Resolved configuration and seeds
- Selected checkpoint, metrics, and artifact hashes

## 33. Parameter count and artifact size
- Count only parameters with requires_grad when reporting trainable size
- Parameter count does not include activation memory
- Checkpoint size can exceed raw parameter bytes because it includes optimizer state
- Report the measured file size and the exact checkpoint contents

## 34. Notebook investigation
```python
python lecture_09_experiments.py
# or open ANN_Lec_9_live.ipynb
```
- Inspect module and state-dict names
- Verify two seeded loaders produce the same index order
- Save and reload weights for prediction equivalence
- Resume Adam training with restored random state
- Compare final logits and model hashes

## 35. Project checkpoint
- Refactor the baseline into a module, data pipeline, and train/evaluate functions
- Save the best validation checkpoint
- Add a fresh-process reload test
- Commit the resolved configuration and an experiment record

## 36. Concept check
- Why can an unregistered tensor disappear from state_dict?
- Which state does Adam require for a faithful resume?
- Why does a fixed seed not guarantee identical results on every platform?
- What does a prediction-equivalence test establish?

## 37. Lecture synthesis
- Modules define ownership of computation and state
- Datasets and loaders separate examples from sampling order
- Device handling belongs at explicit boundaries
- A verified checkpoint makes an interrupted experiment auditable

## 38. Reserve: persistent buffers
- Use register_buffer for tensor state that follows the module across devices
- Persistent buffers enter state_dict without becoming optimizer parameters
- Document whether a buffer is learned, estimated, or fixed

## 39. Reserve: data-pipeline performance
- Increase workers only after correctness is established
- Measure loader time, device utilization, and memory pinning on the target system
- Preserve the split and transformation semantics during performance tuning
