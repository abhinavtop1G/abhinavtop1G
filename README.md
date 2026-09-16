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

I'm Abhinav, a second-year Computer Science student at **Thapar Institute of
Engineering and Technology**, Patiala.

I like understanding *why* something works, not just getting it to work. Most of my
time goes into AI and machine learning 

Outside of that I play chess at state level, which has taught me more about patience
than any amount of debugging ever has.

- 🎓 Second-year **B.E. Computer Science** at Thapar Institute, Patiala
- ♟️ State-level chess player
- 💬 Happy to talk about ML, chess, or getting started with either

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
- 👥 **Core Developer, AI/ML Department** at Google Developer Groups, TIET — run
  community learning initiatives, workshops and peer study groups, translating papers
  and library docs into runnable examples for newer students

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
