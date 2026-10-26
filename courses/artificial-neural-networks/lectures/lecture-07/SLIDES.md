# SE-801 Lecture 7: Optimization Algorithms and Learning Dynamics
## 1. Optimization algorithms and learning dynamics
- How the update rule changes the path across a loss surface

**Source:** https://en.d2l.ai/chapter_optimization/index.html

## 2. Learning outcomes
- Distinguish batch, stochastic, and minibatch gradient estimates
- Compute one momentum and one Adam update
- Diagnose poor conditioning, noisy updates, and an unstable learning rate
- Compare optimizers under the same initialization and update budget
- Defend an optimizer choice with controlled evidence

## 3. Optimization within the learning system
- The model and loss define the objective
- Backpropagation supplies the current gradient
- The optimizer converts gradient history into a parameter update
- Validation evidence judges the training recipe

## 4. One update, three separate choices
- Direction comes from the gradient or a transformed gradient
- Step scale comes from the learning rate and optimizer state
- Gradient evidence comes from a batch of examples
- Changing any one choice can alter the training path

## 5. The empirical-risk gradient
`g(theta) = (1/N) sum_i grad_theta l_i(theta)`
- Full-batch gradient descent uses every training example before one update.
- It is deterministic for fixed parameters and data order.

## 6. Stochastic and minibatch estimates
`g_B(theta) = (1/|B|) sum_{i in B} grad_theta l_i(theta)`
- A single example gives a high-variance estimate.
- A minibatch reduces variance while retaining frequent updates.
- A full batch removes sampling noise but can make each update expensive.

**Source:** https://en.d2l.ai/chapter_optimization/minibatch-sgd.html

## 7. Student calculation: two batch gradients
- Per-example gradients are g1 = [2, 0], g2 = [0, 2], g3 = [2, 2], g4 = [-2, 0]
- Calculate the full-batch mean gradient
- Calculate the mean for minibatch {1, 4}
- Explain why both can be valid estimates but lead to different steps

## 8. Batch-gradient answer
- Full batch: [0.5, 1.0]
- Minibatch {1, 4}: [0, 0]
- The minibatch has no useful direction at this parameter value
- Sampling noise changes the step, not the objective being estimated

## 9. Batch size changes more than memory use
- Small batches provide more updates per pass through the data
- Large batches reduce gradient noise and improve vectorized throughput
- The best choice depends on hardware, data, and the learning rate
- Compare equal examples processed or equal updates, then state which budget you used

**Source:** https://en.d2l.ai/chapter_optimization/minibatch-sgd.html

## 10. Gradient noise as a diagnostic
- Measure gradients for many sampled batches at the same parameters
- Compare their norms and directions with the full gradient
- Large disagreement signals a noisy update estimate
- Noise can help movement, but it can also obscure progress near a minimum

## 11. Poor conditioning creates a narrow valley
`f(x, y) = 0.5 (0.2 x^2 + 8 y^2)`
- The y direction is forty times steeper than the x direction.
- One global learning rate must remain stable in the steep direction.
- Progress along the shallow direction can then become slow.

## 12. Gradient descent on the quadratic
`theta_t = theta_(t-1) - eta g_t`
- grad f = [0.2x, 8y]
- With eta = 0.12, y changes rapidly while x contracts slowly
- The trajectory can zigzag across a narrow valley
- Feature scaling and normalization can improve the geometry seen by the optimizer

## 13. Student calculation: two SGD steps
- Start at theta0 = [4, 1]
- Use f(x,y) = 0.5(0.2x^2 + 8y^2) and eta = 0.1
- Calculate theta1 and theta2
- Which coordinate limits a larger stable learning rate?

## 14. Two-step answer
- g0 = [0.8, 8.0], so theta1 = [3.92, 0.20]
- g1 = [0.784, 1.60], so theta2 = [3.8416, 0.04]
- The steep y direction constrains the learning rate
- The shallow x direction still moves slowly

## 15. Momentum stores a velocity
`v_t = beta v_(t-1) + g_t    theta_t = theta_(t-1) - eta v_t`
- Repeated directions accumulate.
- Alternating directions can partly cancel.
- The state v_t makes the next update depend on earlier gradients.

**Source:** https://en.d2l.ai/chapter_optimization/momentum.html

## 16. Student calculation: one momentum update
- beta = 0.9, eta = 0.1
- Previous velocity v = [1, -2]
- Current gradient g = [3, 4]
- Calculate the new velocity and parameter change

## 17. Momentum answer
- v_new = 0.9[1, -2] + [3, 4] = [3.9, 2.2]
- Parameter change = -0.1 v_new = [-0.39, -0.22]
- The first coordinate reinforces earlier motion
- The second coordinate reverses only after overcoming stored velocity

## 18. Momentum changes the trajectory
- A useful beta preserves consistent progress
- Too much velocity can overshoot or oscillate
- Learning rate and momentum must be interpreted together
- Optimizer state must be saved when training resumes

## 19. Adaptive coordinate scaling
- Some parameters repeatedly receive large gradients
- Others receive small or sparse gradients
- Adaptive methods maintain a separate scale for each coordinate
- The effective step still depends on a global learning rate

## 20. Adam maintains two moving averages
`m_t = beta1 m_(t-1) + (1-beta1)g_t    s_t = beta2 s_(t-1) + (1-beta2)g_t^2`
- m_t estimates a smoothed first moment.
- s_t estimates a smoothed second raw moment.
- Bias correction matters when both states start at zero.

**Source:** https://en.d2l.ai/chapter_optimization/adam.html

## 21. Adam update after bias correction
`theta_t = theta_(t-1) - eta m_hat_t / (sqrt(s_hat_t) + epsilon)`
- Coordinates with persistent large squared gradients receive smaller scaled steps.
- Adam often reduces early tuning effort, but it does not remove the need for controlled comparison.

## 22. Student calculation: Adam at the first step
- g1 = [2, -4], beta1 = 0.9, beta2 = 0.999
- m0 = 0, s0 = 0, eta = 0.01, ignore epsilon
- Calculate m1, s1, their bias-corrected values, and the parameter change

## 23. First-step Adam answer
- m1 = [0.2, -0.4] and s1 = [0.004, 0.016]
- m_hat1 = [2, -4] and s_hat1 = [4, 16]
- The scaled direction is [1, -1]
- Parameter change = [-0.01, +0.01]

## 24. Learning-rate schedules
- A constant rate makes interpretation simple
- Step decay changes the rate at specified milestones
- Cosine decay changes it smoothly over a fixed budget
- Warmup limits early steps before the optimizer state becomes informative
- The schedule belongs in the recorded training recipe

**Source:** https://en.d2l.ai/chapter_optimization/lr-scheduler.html

## 25. Break
- 20 minutes
- After the break: controlled optimizer evidence and diagnosis

## 26. A fair optimizer comparison
- Hold the data split, model, initialization, and update budget fixed
- Use the same batch sequence when the comparison requires it
- Tune learning rates without consulting the test set
- Report the selected rule and the full learning curves

## 27. Controlled classification experiment
| Control | Value |
|---|---|
| Initialization | Identical parameter tensors |
| Data order | Identical seed and batch size |
| Budget | 80 epochs |
| Metric | Validation cross-entropy |

- Task: three-class spiral data generated locally
- Model: 2 to 32 to 32 to 3 ReLU MLP
- Budget: the same epochs and minibatches for all optimizers
- Selection: lowest validation cross-entropy
- Test set: evaluated after each recipe is frozen

## 28. Same budget, different learning curves
- Read the early speed, stability, and final validation loss separately
- A faster start does not guarantee the best selected checkpoint
- One synthetic task cannot establish a universal optimizer ranking

## 29. Reference-run results

## 30. Diagnosing a plateau
- Check whether gradients are near zero or merely noisy
- Inspect activation scale and the first-layer gradient
- Compare training and validation loss
- Try a learning-rate range before changing the architecture

## 31. Diagnosing unstable updates
- Loss spikes can indicate a learning rate that is too large
- Non-finite values require an immediate numerical check
- Gradient norms reveal whether clipping would address the symptom
- Clipping does not repair a wrong loss or invalid data scale

## 32. Optimizer choice is an experimental decision
- SGD offers a simple baseline and transparent state
- Momentum can accelerate consistent directions
- Adam provides coordinate-wise scaling and useful defaults
- The evidence should include tuned settings, compute budget, and variability

## 33. Notebook investigation
```python
python lecture_07_experiments.py
# or open ANN_Lec_7_live.ipynb
```
- Run the quadratic trajectory comparison
- Measure gradient variability at four batch sizes
- Train SGD, momentum, and Adam under the frozen protocol
- Change one learning rate and predict the curve before rerunning

## 34. Project checkpoint
- Commit the verified train, validation, and test split
- Record one baseline result with its configuration
- State the optimizer, learning rate, batch size, and budget
- Add one diagnostic plot that can falsify your training claim

## 35. Concept check
- Why does a smaller batch produce a noisier gradient estimate?
- What state does momentum add to plain SGD?
- Why must Adam still use a validation protocol?
- What must remain fixed in an optimizer comparison?

## 36. Lecture synthesis
- Backpropagation supplies a gradient at the current parameters
- Batch selection controls the noise in that gradient estimate
- Optimizer state changes how gradients become updates
- Learning curves and diagnostics support the final choice

## 37. Reserve: saddle points and flat directions
- A small gradient can occur away from a minimum
- Curvature can differ sharply across directions
- Noise and momentum may help leave a flat region
- The local picture remains a diagnostic aid, not a proof of global behavior

## 38. Reserve: gradient clipping
- Clip by value or by global norm when the training recipe requires it
- Record the threshold and the unclipped gradient norm
- Use clipping to control extreme steps, not to hide a broken pipeline
