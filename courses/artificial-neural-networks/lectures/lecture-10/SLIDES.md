# SE-801 Lecture 10 — Convolutional Neural-Network Fundamentals

## Slide 1: Convolutional neural-network fundamentals

- Local structure, shared parameters, and controlled evidence

<!-- Speaker note: Open with the central question: what assumptions make convolution suitable for images and local signals? Do not begin with architecture names. -->

## Slide 2: Learning outcomes

- Compute a two-dimensional cross-correlation by hand
- Calculate output shapes and trainable parameters
- Trace tensors through a compact CNN
- Explain locality, parameter sharing, and translation structure
- Evaluate a CNN against a controlled baseline

<!-- Speaker note: Students should be able to calculate, implement, and defend design choices. Historical architecture recall is not an outcome. -->

## Slide 3: The learning system remains unchanged

- data
- model
- logits
- loss
- gradient
- update
- evaluation

<!-- Speaker note: Connect to Lectures 1 to 5. A CNN changes the model's internal structure. Cross-entropy, optimization, and evaluation still play their previous roles. -->

## Slide 4: Images have spatial structure

- Nearby pixels often describe the same local pattern
- A useful pattern can occur at many positions
- Channels carry aligned measurements at each location
- Flattening discards the explicit neighbourhood structure

<!-- Speaker note: Use a small image grid on the board. Ask what changes when the image shifts by one pixel and what should remain recognizable. -->

## Slide 5: A dense layer scales with image area

- Input: 224 × 224 × 3 = 150,528 values
- Dense output: 1,000 units
- Weights alone: 150,528,000
- The layer learns separate weights for every location

<!-- Speaker note: Students calculate the weight count before the answer appears. The point is both parameter cost and the absence of shared local structure. -->

## Slide 6: Locality and parameter sharing

- A small kernel reads one neighbourhood at a time
- The same kernel is reused at every valid location
- Each output value measures local agreement with that kernel

<!-- Speaker note: Introduce the two assumptions separately. Locality limits what one output sees. Sharing gives the same detector at different positions. -->

## Slide 7: Two-dimensional cross-correlation

- Place the kernel over one input patch
- Multiply corresponding entries
- Sum the products to produce one output value
- Move the kernel and repeat

<!-- Speaker note: D2L Section 7.2. Deep-learning libraries generally compute cross-correlation even though the layer is named convolution. -->

## Slide 8: Student calculation: one output value

- Input patch: [[0, 0], [0, 1]]
- Kernel: [[1, -1], [1, -1]]
- Calculate the elementwise products and their sum

<!-- Speaker note: Pause before revealing. The products are 0, 0, 0, and -1. The output is -1. -->

## Slide 9: One complete cross-correlation

- A 5 × 5 input and a 2 × 2 kernel produce a 4 × 4 output
- Strong negative responses mark the vertical transition
- The response location preserves spatial information

<!-- Speaker note: Run notebook Section 1 after students predict where the nonzero response will appear. The manual and PyTorch outputs match exactly. -->

## Slide 10: The kernel values are learned parameters

- A hand-designed edge kernel demonstrates the operation
- A CNN learns kernels from the task loss
- Backpropagation accumulates evidence from every location where a shared kernel was used

<!-- Speaker note: Connect shared parameters to gradient accumulation. Full matrix backpropagation belongs to Lecture 6, but the dependency can be stated now. -->

## Slide 11: Output size for one spatial dimension

- n_out = floor((n + 2p - d(k - 1) - 1) / s) + 1
- n: input size    k: kernel size
- p: padding       s: stride       d: dilation

<!-- Speaker note: Derive the valid starting positions first for dilation 1, then show the general formula. Apply the same calculation independently to height and width. -->

## Slide 12: Student calculation: four output sizes

- 28, kernel 3, padding 0, stride 1
- 28, kernel 3, padding 1, stride 1
- 28, kernel 5, padding 2, stride 2
- 16, kernel 3, padding 1, stride 2

<!-- Speaker note: Give four minutes. Ask students to show substitution into the formula rather than report only the answer. -->

## Slide 13: Output-size answers

- 26
- 28
- 14
- 8

<!-- Speaker note: Verify using notebook Section 2. Ask why the stride-2 cases roughly halve the size and why padding 1 preserves size for a 3-wide kernel. -->

## Slide 14: Padding controls boundary treatment

- Without padding, border pixels participate in fewer patches
- Padding can preserve spatial size
- Padding values become part of the model's boundary assumption

<!-- Speaker note: Draw a 4×4 input with a one-cell border. Mention zero padding as the common default, not a universal truth. -->

## Slide 15: Stride controls sampling density

- Stride 1 evaluates neighbouring kernel positions
- Larger stride reduces spatial resolution
- Downsampling can lower compute but may discard small features

<!-- Speaker note: Use the same input and kernel with stride 1 and 2. Ask which locations are never evaluated under stride 2. -->

## Slide 16: Channels change the kernel shape

- Input tensor: batch × input channels × height × width
- One output channel uses one kernel slice per input channel
- The channel responses are summed before adding one bias
- Multiple output channels learn different feature maps

<!-- Speaker note: For RGB input and 16 output channels, the weight tensor has shape [16, 3, kH, kW]. Keep batch outside the parameter shape. -->

## Slide 17: Student calculation: multichannel output

- Input shape: [8, 3, 32, 32]
- Layer: Conv2d(3, 16, kernel_size=3, padding=1)
- Find the output shape
- Find the number of trainable parameters

<!-- Speaker note: Answer: [8,16,32,32]. Parameters: 16×3×3×3 + 16 = 448. -->

## Slide 18: Convolution parameter count

- weights = output channels × input channels × kernel height × kernel width
- biases = output channels when bias is enabled
- Spatial input size changes compute and activation memory, not the kernel parameter count

<!-- Speaker note: Contrast with the dense layer. Ask which quantities change the learned weight tensor and which only change the number of output positions. -->

## Slide 19: Student calculation: two convolution layers

- Layer 1: Conv2d(1, 8, 3, padding=1)
- Layer 2: Conv2d(8, 12, 3, padding=1)
- Calculate each layer's parameters and the total

<!-- Speaker note: Allow four minutes. Layer 1 has 80 parameters. Layer 2 has 876. The two convolution layers total 956. -->

## Slide 20: Translation equivariance

- A shifted input tends to produce a shifted feature map
- Shared kernels preserve the identity of a local detector
- Boundary effects and downsampling make the relationship approximate in practical networks

<!-- Speaker note: Use equivariance accurately. The feature map shifts with the input. That differs from invariance, where an output remains unchanged. -->

## Slide 21: Pooling and invariance

- Max pooling retains the strongest value in each window
- Average pooling retains the local mean
- Pooling reduces resolution and can make small shifts less consequential
- Aggressive pooling can remove information

<!-- Speaker note: D2L Section 7.5. Avoid claiming that pooling guarantees full translation invariance. -->

## Slide 22: Student calculation: max pooling

- Input: [[1, 3, 2, 0], [4, 6, 5, 1], [0, 2, 7, 8], [1, 3, 4, 9]]
- Use a 2 × 2 window with stride 2
- Calculate the 2 × 2 output

<!-- Speaker note: Answer: [[6,5],[3,9]]. Ask which input locations receive gradient under max pooling when every maximum is unique. -->

## Slide 23: Receptive field

- A unit's receptive field is the input region that can affect it
- Stacked local layers expand the receptive field
- Stride increases the spacing between neighbouring receptive fields

<!-- Speaker note: For stride-1 3×3 layers, one layer sees 3×3, two see 5×5, and three see 7×7. Explain overlap. -->

## Slide 24: Break

- 20 minutes
- After the break: PyTorch, controlled evidence, and debugging

<!-- Speaker note: Keep the output-size formula and parameter-count formula visible on the board. -->

## Slide 25: The `Conv2d` contract

- Input: [N, C_in, H, W]
- Weights: [C_out, C_in / groups, kH, kW]
- Bias: [C_out]
- Output: [N, C_out, H_out, W_out]

<!-- Speaker note: Point out that PyTorch uses channels-first tensors. Print layer.weight.shape during the live demonstration. -->

## Slide 26: Manual and framework results agree

- The loop implementation and `F.conv2d` use the same input and kernel
- Maximum absolute difference: 0.0
- Shape and numerical equivalence provide a focused implementation check

<!-- Speaker note: Run notebook Section 1. This verifies one single-channel valid cross-correlation case, not every Conv2d option. -->

## Slide 27: Synthetic orientation task

- Class 0 contains a vertical bar
- Class 1 contains a horizontal bar
- Noise and intensity vary independently
- Training positions and shifted test positions do not overlap

<!-- Speaker note: Run notebook Section 3. The experiment isolates translation structure rather than claiming performance on natural images. -->

## Slide 28: Controlled evaluation protocol

- 800 training examples with central positions
- 200 validation examples with the same position range
- 200 frozen test examples near the image boundaries
- The test set is opened after model selection

<!-- Speaker note: Ask why random splitting all positions together would fail to test translation transfer. Connect to leakage and distribution shift from Lecture 3. -->

## Slide 29: Two models with similar parameter budgets

- MLP: flatten, 4 hidden units, 2 logits, 1,038 parameters
- CNN: two convolutions, global average pooling, 2 logits, 982 parameters
- Both use the same split, loss, epoch budget, and checkpoint rule

<!-- Speaker note: Similar parameter counts reduce one confound. The architectures still differ in optimization geometry, so this is a controlled comparison rather than a proof that parameter count is the only cause. -->

## Slide 30: Student calculation: CNN shape trace

- Input: [2, 1, 16, 16]
- Conv2d(1, 8, 3, padding=1)
- MaxPool2d(2)
- Conv2d(8, 12, 3, padding=1)
- AdaptiveAvgPool2d((1,1)), flatten, Linear(12,2)

<!-- Speaker note: Students write every intermediate tensor shape. Require the batch dimension in every answer. -->

## Slide 31: CNN shape trace

- [2,1,16,16]   input
- [2,8,16,16]   first convolution
- [2,8,8,8]     max pooling
- [2,12,8,8]    second convolution
- [2,12,1,1]    global average pooling
- [2,12] then [2,2]   flatten and classifier

<!-- Speaker note: Run notebook Section 4. Check that students do not flatten before global pooling or lose the batch dimension. -->

## Slide 32: Validation accuracy alone misses the shift

- MLP validation: 100.0%
- CNN validation: 100.0%
- Both models solve the in-distribution validation task
- The shifted test asks a different scientific question

<!-- Speaker note: Do not reveal the test result until students predict it. Ask which model encodes a reason to transfer across position. -->

## Slide 33: The shifted test separates the models

- MLP shifted-test accuracy: 0.0%
- CNN shifted-test accuracy: 100.0%
- The MLP fitted central locations but did not transfer to unseen boundary positions
- The CNN reused local orientation detectors across the image

<!-- Speaker note: These results apply only to the frozen synthetic protocol. They demonstrate the effect of a useful inductive bias, not universal CNN superiority. -->

## Slide 34: Learning curves support the diagnosis

- Both validation curves converge
- The validation distribution contains only central bar positions
- A learning curve cannot reveal an unmeasured deployment shift

<!-- Speaker note: Run notebook Section 6. Connect the result to the earlier distinction between validation performance and the target population. -->

## Slide 35: Feature maps retain spatial evidence

- Different channels respond to different learned patterns
- The activation remains indexed by spatial location
- A feature map is evidence for interpretation, not a complete explanation

<!-- Speaker note: Show one shifted test image and its first-layer maps. Avoid assigning semantic names without a controlled intervention. -->

## Slide 36: One-dimensional convolution uses the same logic

- The kernel slides over time rather than height and width
- Input channels can represent sensors, electrodes, or frequency bands
- Local temporal patterns can be reused across a recording
- Valid evaluation may require subject-wise or session-wise splits

<!-- Speaker note: Connect to EMG, EEG, PCG, vibration, and acoustic signals. Keep the split warning explicit for repeated measurements. -->

## Slide 37: Common implementation errors

- Wrong axis order: NHWC supplied where NCHW is expected
- Incorrect flatten size after convolution or pooling
- Softmax applied before `CrossEntropyLoss`
- Validation or test data used to tune the architecture
- A claimed invariant property without a shifted evaluation set

## Slide 38: Concept check

- Why does parameter sharing reduce parameters?
- What is the output of Conv2d(3,16,3,padding=1) for [8,3,32,32]?
- How many parameters does that layer contain?
- How do equivariance and invariance differ?
- What split would test translation transfer?

## Slide 39: Lecture synthesis

- Convolution encodes locality and parameter sharing
- Padding, stride, channels, and pooling determine tensor shapes
- Parameter counts depend on channel counts and kernel size
- Controlled shifts test whether the intended inductive bias helps

<!-- Speaker note: Return to the central question. Ask one student to explain when a CNN would be a poor default choice. -->

## Slide 40: Project checkpoint

- State the structure your model assumes
- Show every tensor shape through the first forward pass
- Compare against a simpler baseline under the same split
- Report parameters and one failure mode

<!-- Speaker note: For image projects use a compact CNN baseline. For sensor projects justify whether 1D convolution matches the sampling and channel structure. -->

## Slide 41: Reserve: grouped and depthwise convolution

- Groups restrict which input channels connect to which outputs
- Depthwise convolution uses one spatial kernel per input channel
- A pointwise 1 × 1 convolution can then mix channels
- Efficiency gains depend on hardware and implementation

<!-- Speaker note: Use only if time remains. This previews later efficient design without making it core assessment material today. -->

## Slide 42: Reserve: general receptive-field recurrence

- jump_l = jump_(l-1) × stride_l
- receptive_l = receptive_(l-1) + (kernel_l - 1) × dilation_l × jump_(l-1)
- Start with jump 1 and receptive field 1 at the input

<!-- Speaker note: Work one example containing stride 2 only if the core lecture finishes early. -->
