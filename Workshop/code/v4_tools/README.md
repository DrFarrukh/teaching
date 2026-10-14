# Session 1 — V4

Independent Sol implementation, based only on `AI_Workshop_Session1_v2.pptx`.
No subagents were used. V1, V2, V3, the shared deck tools and `code/outputs/`
were not edited. No Git commit was made.

## Deliverables

- `../../AI_Workshop_Session1_v4.pptx` — 68 slides; opening logo slide removed.
- `../v4_outputs/slide_map.md` — current V4 numbers mapped to the user's V2 numbers.
- `../v4_outputs/manifest.json` — model identities, checkpoint hashes, executed
  inference, feature tensors/layer selections and recorded lab provenance.
- `../v4_outputs/verification.json` — executed acceptance checks.
- `../v4_outputs/evidence/` — preserved training histories/source figures and
  numerical calculations; not newly trained models.

Generated slide figures and GIFs are under `code/v4_outputs/`. The three pixel
grid slides remain separate (V4 slides 4–6) for the presenter to merge.

## Reproduction

Run from the repository root using the requested `~/ml` environment:

```bash
# Only needed if these three weights are absent; explicitly authorized for V4.
~/ml/bin/python code/v4_tools/prefetch_weights.py

# The supplied executed notebook and gallery are available at this location.
# Check GPU occupancy before selecting CUDA; use --device cpu if occupied.
~/ml/bin/python code/v4_tools/generate_figures.py --device cuda \
  --lab-dir /tmp/opencode/workshop_src/Session1/Lab

~/ml/bin/python code/v4_tools/build_deck.py
~/ml/bin/python code/v4_tools/verify_deck.py
```

For a later checkout where the external notebook is no longer available, keep
the `v4_outputs/evidence/` files and `v4_outputs/source/` photographs, then use:

```bash
~/ml/bin/python code/v4_tools/generate_figures.py --device cpu --reuse-lab-evidence
~/ml/bin/python code/v4_tools/build_deck.py
~/ml/bin/python code/v4_tools/verify_deck.py
```

No training is performed by any V4 script. Inference loads local, hash-checked
checkpoint files with `weights=None` and `weights_backbone=None`. It cannot
implicitly download weights. Only `prefetch_weights.py` downloads the three
specifically authorized checkpoints (MobileNetV3-Small, SSDLite, LR-ASPP).

Required packages already present in `~/ml`: torch, torchvision, numpy, Pillow,
matplotlib, OpenCV, python-pptx and lxml. Rendering uses the existing LibreOffice
wrapper and Poppler, without installations.

## Acceptance criteria

1. Preserve V2; write only V4-specific repository files and review temporaries.
2. Apply the requested removals, above/below image layouts, grayscale swatches,
   three successive pixel grids, photo-based filtering/template matching,
   horizontal flip, simplified detection and IoU, supplied weed example,
   merged ReLU/pooling and enlarged/minimal-text model outputs.
3. Put extracted pretrained CNN activations **after** ReLU/pooling; connect the
   same model's input, selected maps, pooled vector and classification scores.
4. Use the named models on slides 55–57 (V2 numbering); never substitute another
   detector/segmenter while retaining the original model title.
5. Correct multi-label/detection confusion, ground-truth claims, connected-
   component versus instance-model claims, annotation versus prediction,
   classifier universality and the explanation of the fence error.
6. Preserve historical training provenance; no newly invented metrics, training
   or universal transfer-learning claims. Use native editable learning charts.
7. Verify numerical operations, image-source correspondence, package structure,
   GIF bytes/frames, slide ordering and rendered appearance.

Follow-up: the former V4 slide22 now compares square, circle and oval outlines
through an animated search and similarity heatmap. It becomes slide21 after
removing the opening logo slide. The four embedded GIFs are numerically checked.

## Scientific distinctions

- The convolution GIF is a **fixed edge-kernel calculation**, not a claimed
  trained kernel. Its window arithmetic is saved in `evidence/convolution.json`.
- Geometric templates search the full Canny edge image without restricting the
  search to eyes. Their scores and locations are computed, not hand-picked.
  Correlation is similarity, not eye-detection probability. Square/oval can
  select non-eye regions; the circle overlaps one eye in this demonstration.
- The pooling GIF uses a captured ResNet18 ReLU activation patch. Its 3×3,
  stride-2 maxima are checked against the model's captured max-pooling output.
- Feature channels are selected by spatial variance and individually scaled
  for display. They are not labelled “eye”, “fur” or attributed semantic roles.
- The 512-element pooled vector and ImageNet head reconstruct the captured
  classification logits within `1e-5`; this is evidence of the forward path,
  not a complete explanation of the classification decision.
- IoU compares disclosed **illustrative** rectangles; no human-ground-truth
  evaluation is claimed.
- Separate cat components illustrate instance separation but were not generated
  by an instance-segmentation network. That distinction appears on the slide.
- Training curves and the 3-class head example come from the executed notebook.
  The original lab reports test accuracy each epoch; V4 teaches the distinction
  between validation for development and a final untouched test evaluation.
- Confusion counts were visually transcribed from the preserved source PNG and
  checked against its class supports and the recorded final accuracy. The
  source hash and computed statistics are in `evidence/confusion_counts.json`.
- The notebook's trained 3-class checkpoint was not supplied. The recorded
  head prediction is therefore not represented as newly rerun inference.
- Model failures are retained: SSDLite mislabels a dog as cat in the mixed
  photograph; Faster R-CNN mislabels the fluffy dog; DeepLab mislabels fence
  pixels as chair.

## Image provenance and remaining limits

Existing pet-image credits are in `code/assets/CREDITS.md`. They are used as
supplied attribution, not an independent license audit. The supplied weed
photographs/overlays lack an accompanying class-name legend and model/evaluation
record. V4 uses those images without guessing class names or repeating the
embedded `mIoU 0.723` as a verified result. The annotation example is cropped
from the user-supplied panel labelled “Ground truth”.

The source gallery's bus photograph is preserved for reproduction; original
photographer/license details should be confirmed before public redistribution.
No datasets or credentials were copied into prompts.

GIF frames and their byte-for-byte inclusion are verified. LibreOffice renders
the first (completed) frame for PDF export. Interactive playback in the user's
PowerPoint/Impress slideshow application remains a final presentation check.

## Execution checkpoint

- Prefetch: exit 0; all three authorized downloads verified by SHA-256 prefix.
- Figure generation: exit 0 using `~/ml/bin/python` and CUDA on the idle GPU.
- Build: successful V4-specific builds; 68 slides after the logo-slide removal,
  source V2 hash unchanged.
- Acceptance verification: successful report in `v4_outputs/verification.json`.
- OOXML validation with V2 baseline: all validations passed.
- Rendering: exit 0; review PDF/JPEGs in `/tmp/opencode/workshop-v4-review/`.
- Visual review: the original 69-slide V4 inspected through contact sheets; identified
  contour/pooling clarity, table-word wrapping and header/caption spacing issues
  were corrected, re-rendered and checked at full size.

Initial implementation errors (font lookup, executed-notebook location,
inference-context handling and slide-part API access) were corrected before the
successful runs. No failed command is counted as validation evidence.

Next step: presenter review of V4, especially animated playback and supplied
weed class names. Do not overwrite V2/V3 or launch further training automatically.
