# V2 → V4 slide map

| V4 | V2/source | Title |
|---|---|---|
| 1 | 2 | What do you see? |
| 2 | 3 | Cat · Fur · Eyes · Whiskers… / 2 / 68 |
| 3 | 4 | A photograph is a grid of pixels |
| 4 | 5 | A small patch of the image |
| 5 | 5b | Each pixel has a brightness value |
| 6 | 5c | The image is a matrix of numbers |
| 7 | 7 | 0 is black. 255 is white. |
| 8 | 8 |  / 01 / IMAGE AS DATA / What changes when resolution changes? / Same photograph. Fewer samples. Less detail. /  / 16 pixels wide / |
| 9 | 9 |  / 01 / IMAGE AS DATA / Colour = three channels, not one. / Red, green and blue intensities form one RGB image. /  / Red channel / |
| 10 | 12 |  / 01 / IMAGE AS DATA / Models require consistent inputs. / Resize, scale numerical values and form batches. /  / 01 / READ IMAGE  |
| 11 | 13 |  / 01 / IMAGE AS DATA / All three are numbers to the model. / Full colour, grayscale and edge maps — same scene, different arrays. |
| 12 | 14 |  /  / 02 / CLASSICAL COMPUTER VISION / Before deep learning, we processed images. / Filters · thresholds · contours · templates /  |
| 13 | 15 |  / 02 / CLASSICAL VISION / Brightness and contrast change pixels. / Useful preprocessing ≠ object understanding. /  / Lower bright |
| 14 | 16 |  / 02 / CLASSICAL VISION / Smoothing can remove noise. / A filter combines neighboring pixel values. /  /  / NOISY / HIGH DETAIL / |
| 15 | 17 |  / 02 / CLASSICAL VISION / Edges mark rapid changes. / A classical edge detector is not a cat detector. /  /  / ORIGINAL RGB IMAGE |
| 16 | 18 |  / 02 / CLASSICAL VISION / Thresholding makes a pixel decision. / A numerical rule converts grayscale into a binary mask. /  /  /  |
| 17 | 19 | Contours describe boundaries |
| 18 | 20 |  / 02 / CLASSICAL VISION / Colour thresholds isolate regions. / A simple rule can find orange regions—until lighting changes. /  / |
| 19 | 20b | A colour rule applied to a photograph |
| 20 | 21 |  / 02 / CLASSICAL VISION / Template matching searches for a pattern. / A reference patch is compared across candidate image locati |
| 21 | 21b | Can simple shapes find the eyes? |
| 22 | 22 |  / 02 / CLASSICAL VISION / The classic computer vision pipeline / Engineered features + designed decision rules. /  / 01 / CAPTURE |
| 23 | 23 | The same scene can look different |
| 24 | 24 |  / 02 / CLASSICAL VISION / Instead of handcrafting every rule... / What if the system learns useful visual features from examples? |
| 25 | 25 |  /  / 03 / CORE COMPUTER VISION TASKS / One image. Three different questions. / Classification · Object detection · Segmentation / |
| 26 | 26 | Classification: what is in this image? / Cat / 26 / 68 |
| 27 | 27 | A classifier produces class scores |
| 28 | 28 | Single-label versus multi-label |
| 29 | 29 | Detection: what objects—and where? |
| 30 | 30 | One detection, three components |
| 31 | 31 | 03 / DETECTION / Teal: box A · Orange: box B · Shading: overlap / IoU = overlap area / union area = 0.58 / Two illustrative boxes; |
| 32 | 32 | 03 / SEGMENTATION / Input / Predicted class mask / Segmentation: which pixels belong to each class? / 32 / 68 |
| 33 | 33 |  / 03 / SEGMENTATION / Semantic segmentation labels each pixel. / All pixels of one class receive the same category label. /  /  / |
| 34 | 34 | Semantic classes versus separate instances |
| 35 | 35 | One photograph. Three outputs. |
| 36 | 36 | The task determines the annotation |
| 37 | 38 | From field photograph to segmentation |
| 38 | 39 |  / 03 / CHOOSING THE TASK / Match the task to the output you need. / Each scenario asks for a different kind of answer. /  /  / ?  |
| 39 | 40 |  /  / 04 / DEEP VISUAL LEARNING / How does a neural network learn to see? / From handcrafted filters to learned representations /  |
| 40 | 41 |  / 04 / FEATURE LEARNING / Classical ML versus deep learning / The defining difference: who designs the features? /  /  / TRADITIO |
| 41 | 42 | A kernel moves across a pixel grid |
| 42 | 43 | The same window moves across the photograph |
| 43 | 46 | ReLU and max pooling transform responses |
| 44 | 44 | Feature maps from a pretrained CNN |
| 45 | 45 | From feature maps to a cat prediction |
| 46 | 48 | Feature maps are responses—not named parts |
| 47 | 49 |  / 04 / CNN BASICS / A CNN has two conceptual stages. / Feature extractor + task-specific output head. /  / 01 / INPUT IMAGE /  /  |
| 48 | 50 |  / 04 / TRAINING / Training is a repeated correction loop. / The model adjusts parameters to reduce prediction error. /  / 01 / EX |
| 49 | 51 | Learning curves help inspect progress |
| 50 | 52 | Separate training, validation and test |
| 51 | 53 |  / 04 / UNIFIED VIEW / Same backbone concept; different output heads. / Classification, detection and segmentation require differe |
| 52 | 54 |  /  / 05 / FROM CONCEPTS TO IMPLEMENTATION / Three compact model examples. / Representative architectures—not claims of 2026 state |
| 53 | 55 | MobileNetV3-Small |
| 54 | 56 | SSDLite320 + MobileNetV3-Large |
| 55 | 57 | LR-ASPP + MobileNetV3-Large |
| 56 | 58 |  / 05 / TRANSFER LEARNING / Reuse visual knowledge. Adapt the final head. / Pretraining can reduce the data and optimization neede |
| 57 | 59 | 06 / LAB AND MODEL OUTPUTS / Train a model. Inspect its outputs. / Recorded lab training, then pretrained models on our photograph |
| 58 | 60 | Train a small CNN from scratch |
| 59 | 61 | Transfer learning performed better here |
| 60 | 62 | Where the classifier still errs |
| 61 | 63 | One top prediction for the whole image |
| 62 | 64 | Confidence is not correctness |
| 63 | 65 | Pixel labels can also be wrong |
| 64 | 66 | One photograph, three different answers |
| 65 | 67 |  / 07 / HANDOFF / Now you will build a working classifier. / The lab engineer leads the coding and model training. /  / 01 / OPEN  |
| 66 | 68 | Prediction, learning curve, error analysis |
| 67 | takeaways | Choose the output your problem needs |
| 68 | 69 | References and image sources |