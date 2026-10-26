# SE-801 Lecture 6 Student Guide

Welcome to **Lecture 6: Backpropagation, Parameter Initialization, and Stable Training Dynamics**.

This guide outlines your reading, environment setup, and study route for the week.

---

## 1. Primary Reading & Syllabus Context

* **Primary Textbook:** *Dive into Deep Learning* (D2L.ai), PyTorch Edition.
  * **Section 5.3:** Forward Propagation, Backward Propagation, and Computational Graphs.
  * **Section 5.4:** Numerical Stability and Initialization.
  * **Section 5.6:** Dropout.
* **Core Objective:** Understand why deep neural networks fail to learn when initialized improperly, and derive the exact mathematical mechanics that enable stable reverse-mode gradient descent.

---

## 2. Directory Structure & Materials

Your student folder contains:

```text
ANN_Lecture_06/
├── README.md                           <- Quick-start overview
├── STUDENT_GUIDE.md                    <- This file
├── Lecture_06_Slides.md                <- Markdown slide deck transcript
├── ANN_Lec_6.ipynb                     <- Fully executed notebook with saved plots & outputs
├── ANN_Lec_6_live.ipynb                <- Clean notebook for live coding & prediction pauses
├── Lecture_06_Concept_Check.md         <- 5 ungraded diagnostic questions
├── Practice_and_Project_Checkpoint.md  <- Implementation exercises and project milestone brief
├── data_dictionary.md                  <- Description of synthetic dataset & generated artifacts
└── requirements.txt                    <- Minimal dependencies (torch, numpy, matplotlib)
```

---

## 3. Environment & Running the Notebook

The notebooks run completely offline on a standard laptop CPU. No GPU, remote downloads, or heavy packages are required.

### Setup:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

### Study Route:
1. Open `ANN_Lec_6_live.ipynb`.
2. Before executing each cell, read the **ASK BEFORE RUNNING** prompt. Predict the gradient shape or numerical behavior before revealing the output.
3. Review `outputs/layer_activation_distributions.png` and `outputs/initialization_comparison_curves.png` to inspect how signal variance propagates across deep layers.
4. Complete the 5 questions in `Lecture_06_Concept_Check.md` to verify your mathematical derivation skills before beginning Assignment 2.
