<!--
  GitHub profile README for @abhinavtop1G
  ---------------------------------------
  1. Create a PUBLIC repo named exactly:  abhinavtop1G
  2. Put this file in it as README.md
  3. Swap the ASCII art below for your own (notes at the bottom)
  4. Fill in the three <repo-link> placeholders
  5. Delete this comment block before committing
-->

<h1 align="center">Hi, I'm Abhinav Saini 👋</h1>

<p align="center">
  <b>Computer Science @ Thapar Institute</b> · Core Developer, GDG AI/ML<br>
  I build machine learning systems that run on real data and real hardware.
</p>

```text
       .-------.          abhinav@tiet --------------------------------
     .'#########'.        * OS: ......... Windows 11 / Linux
    /#############\       * Host: ....... Thapar Institute, Patiala
   |###############|      * Kernel: ..... B.E. Computer Science '29
   |##  ---  ---  #|      * Role: ....... Core Dev, GDG AI/ML Dept
   |#             #|      * IDE: ........ VS Code, Jupyter
   |#   :::::::   #|
    \#  :::::::  #/       * Languages: .. Python, C++
     '.:::::::::.'        * ML: ......... PyTorch, TensorFlow, sklearn
       '-------'          * Vision: ..... YOLO, OpenCV, MediaPipe
        |     |           * NLP: ........ DistilBERT, DeBERTa, LangChain
    ..--'-----'--..       * Edge: ....... Raspberry Pi, Ultralytics
  .'  /         \  '.     * Core CS: .... DSA, OOP
 /   /   \   /   \   \
|   |     \ /     |   |   - Contact -----------------------------------
|   |     >#<     |   |   * Email: ...... abhinav.hustler1@gmail.com
|   |    /   \    |   |   * LinkedIn: ... abhinav-saini-46878a373
|   | o |     | o |   |   * Location: ... Patiala, Punjab, India
|   | o |     | o |   |
|   | o |     | o |   |
|   |___|     |___|   |
|_______|     |_______|
```

---

## 🚀 About Me

Second-year CSE student at **Thapar Institute of Engineering and Technology**, working
across **deep learning, computer vision, and edge AI**.

Most of what I build has to survive contact with messy inputs — satellite tiles,
691K-row tabular datasets, live camera feeds on a Raspberry Pi. I care about the part
after the notebook: getting a model to run somewhere constrained, and knowing whether
the number it produced actually means anything.

- 👥 **Core Developer, AI/ML Department** at Google Developer Groups, TIET — I run
  workshops and build starter ML projects for students newer than me
- 💬 Ask me about **YOLO, DistilBERT, gradient boosting, or edge inference**

---

## 📌 Projects

### 🌍 VeriFEarth — AI Audit Layer for Carbon Credit Fraud
An independent verification system that cross-checks carbon-project claims against
**Sentinel-2 satellite imagery**, fusing NLP and remote-sensing signals into a single
**Integrity Score (0–100)**.

- Fine-tuned **DistilBERT (66M params)** on a hand-labelled corpus of environmental
  claims to separate greenwashing from credible language — **0.95 F1** on held-out test
- Trained a logistic-regression classifier on **6 spectral features** (NDVI, NDWI + 4
  Sentinel-2 reflectance bands), running per-pixel inference on real satellite tiles
  through the **Microsoft Planetary Computer STAC API**

`Python` · `DistilBERT` · `scikit-learn` · `Sentinel-2` · `STAC API`

🔗 **[View repository](<repo-link>)**

---

### 📊 Kaggle Playground Series S6E8 — Binary Classification, 691K Rows
A 691K-row, 12-feature binary classification task, finished with a 10-fold
hill-climbed 3-model blend at **0.96561 OOF AUC**.

- Expanded 12 raw columns into **45 engineered features**, and treated missingness as
  signal — with up to **19%** of values absent, encoding *whether* a value was recorded
  beat imputation outright
- Ran **60 Optuna trials** (shallow, heavily regularised trees at `max_depth=3` won),
  then diagnosed a 6-model stack whose 0.988–0.997 level-0 correlations bought only
  **+0.0003 AUC** — and recovered the gains with a tabular neural net whose categorical
  embeddings failed on *different* rows

`Python` · `XGBoost` · `CatBoost` · `Optuna` · `PyTorch`

🔗 **[View repository](<repo-link>)**

---

### 🚗 Real-Time Vehicle Detection — Edge AI for Smart Mobility
A complete edge-inference pipeline for intelligent traffic monitoring, deployed on
**Raspberry Pi**.

- Built YOLO-based real-time vehicle detection running entirely on constrained hardware
- Implemented vehicle tracking on live camera feeds with OpenCV, PyTorch and Ultralytics,
  layering deep-learning analysis on top of detection for cluttered scenes
- Tuned for low-power deployment, cutting computational overhead for energy-efficient
  inference at the edge

`Python` · `YOLO` · `Ultralytics` · `OpenCV` · `Raspberry Pi`

🔗 **[View repository](<repo-link>)**

---

## 🛠️ Technical Skills

**Languages & Core CS**
`Python` `C++` · Data Structures & Algorithms · Object-Oriented Programming

**AI & Machine Learning**
`scikit-learn` `PyTorch` `TensorFlow` `Ultralytics YOLO` `OpenCV` `MediaPipe`
`DistilBERT` `DeBERTa` `LangChain` `RAG`

**Domains & Deployment**
Machine Learning · Deep Learning · Computer Vision · Predictive Modelling ·
Edge AI on Raspberry Pi

**Tools**
`Git` `GitHub` `VS Code` `Jupyter` `Microsoft Planetary Computer (STAC API)`

---

## 🏆 Achievements

- 🥇 **Finalist — HackOWASP**, reaching the finalist stage among **150+ competing teams**
- ♟️ **State-Level Chess Player**, represented at competitive state-level tournaments
- 👥 **Core Developer, GDG AI/ML Department** — run community learning initiatives,
  workshops and peer study groups, translating papers and library docs into runnable
  examples for newer students

---

## 📊 GitHub Stats

<p align="center">
  <img height="165" src="https://github-readme-stats.vercel.app/api?username=abhinavtop1G&show_icons=true&theme=tokyonight&hide_border=true&count_private=true" alt="Abhinav's GitHub stats" />
  <img height="165" src="https://github-readme-stats.vercel.app/api/top-langs/?username=abhinavtop1G&layout=compact&theme=tokyonight&hide_border=true" alt="Top languages" />
</p>

---

## 🤝 Connect

<p align="center">
  <a href="mailto:abhinav.hustler1@gmail.com">
    <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" />
  </a>
  <a href="https://www.linkedin.com/in/abhinav-saini-46878a373/">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
  <a href="https://github.com/abhinavtop1G">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
  </a>
</p>

<!--
  ============================================================
  NOTES - delete this whole block before publishing
  ============================================================

  BEFORE YOU COMMIT
    - Replace the three <repo-link> placeholders with real URLs.
      A project section with a dead link is worse than no link at all.
    - LinkedIn is set to linkedin.com/in/abhinav-saini-46878a373 (verified by you).
    - Your PHONE NUMBER is deliberately NOT here. It's fine on a resume you
      hand to a recruiter, but a GitHub profile is public to the whole
      internet and gets scraped by bots. Add it back only if you want that.

  MAKING THE ASCII PORTRAIT
    Web:  ascii-art-generator.org  (upload photo, set width ~30)
    CLI:  ascii-image-converter -W 30 photo.jpg
    CLI:  jp2a --width=30 photo.jpg

    High-contrast photos convert far better than busy ones.
    Keep it under ~35 chars wide or the right column wraps on phones.
    Align the right column by eye in VS Code, then CHECK IT ON MOBILE.

  WHAT MATTERS MORE THAN THIS FILE
    1. Pin these 3 projects (Profile -> Customize your pins)
    2. Give each pinned repo its own README with a screenshot at the top
    3. Write a real one-line description on every pinned repo

    Your metrics are the strongest thing you have - 0.95 F1, 0.96561 AUC,
    691K rows, 66M params. Make sure they appear in the project READMEs
    too, not just here. Numbers are what separate you from the hundreds of
    profiles that just say "passionate about AI/ML".
-->
