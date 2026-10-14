# Computer Vision Workshop — Session 1

From pixels to classification, object detection and segmentation.

- [PowerPoint slides — V4](AI_Workshop_Session1_v4.pptx)
- [Participant lab notebook](Session1_Lab.ipynb)
- [Open the notebook in Google Colab](https://colab.research.google.com/github/drfarrukh/teaching/blob/main/Workshop/Session1_Lab.ipynb)
- [Figure-generation and authoring code](code/v4_tools/README.md)
- [Slide-number mapping](code/v4_outputs/slide_map.md)
- [Executed verification report](code/v4_outputs/verification.json)

## Slides

68 slides with four embedded animations, extracted CNN activations, model
outputs, editable learning charts and recorded lab results. The opening logo
slide has been removed. Slide21 compares square, circle and oval templates with
an animated search and a similarity heatmap.

Use PowerPoint or Impress **slideshow mode** to play the GIFs. Static previews
display a completed frame. Interactive playback remains a presenter check.

## Notebook

The existing participant notebook is provided unchanged. It includes training,
transfer learning, pretrained-model inference and a three-output demonstration.
It was not executed or retrained during this publication step. Running it may
download data and pretrained weights and use the runtime selected by the user.

## Reproducible figures

Python scripts, their inputs and generated evidence are under `code/`.
`shape_matching.py` independently reproduces the geometric-template animation.
The full deck-authoring pipeline additionally needs the original V2 source deck
from the authoring project; older slide versions are deliberately not published
in this folder. The saved verification report was executed in that project
before transferring the final presentation here.

Historical training results are distinguished from pretrained inference.
Similarity scores and model scores do not guarantee correct object identity.
Image-source notes and remaining attribution/provenance limits are documented
in `code/assets/CREDITS.md` and `code/v4_tools/README.md`.
