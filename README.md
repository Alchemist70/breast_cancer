# Breast Cancer AI Prediction System

## Overview

The **Breast Cancer AI Prediction System** is a full-stack web application that leverages advanced machine learning models to provide comprehensive predictions for various breast cancer outcomes. Designed for clinicians, researchers, and patients, the system offers real-time, batch, and single-case predictions, as well as educational resources and visual analytics.

- **Backend:** FastAPI (Python) serving multiple ML models
- **Frontend:** React (Vite) for a modern, responsive UI
- **Deployment:** Render.com (cloud-ready, one-click deploy)
- **Machine Learning:** Random Forest, Gradient Boosting, and Ensemble models trained on clinical and genomic data

---

## Features

- **Comprehensive Predictions:** Malignancy, cancer type, stage, metastasis, treatment outcome, and more
- **Batch Upload:** Predict outcomes for multiple patients via CSV upload
- **Single Prediction:** Real-time prediction for individual cases
- **Visual Analytics:** Interactive charts and model performance metrics
- **Model Info:** Transparency on model accuracy, features, and limitations
- **Educational Content:** About cancer, risk factors, and trusted resources
- **Downloadable Templates:** Easy-to-use CSV templates for batch predictions

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Alchemist70/breast_cancer.git
cd breast_cancer
```

### 2. Install Python Dependencies

```bash
python -m venv myvenv
source myvenv/bin/activate  # On Windows: myvenv\Scripts\activate
pip install -r requirements.txt
```

### 3. Install Node.js Dependencies and Build Frontend

```bash
cd frontend
npm install
npm run build
cd ..
```

### 4. Run the Application Locally

```bash
uvicorn app:app --reload
```

Visit [http://localhost:8000](http://localhost:8000) in your browser.

---

## Deployment

This project is ready for deployment on [Render.com](https://render.com):

- All necessary build and start commands are in `build.sh` and `render.yaml`.
- Model files are managed with [Git LFS](https://git-lfs.github.com/).

**To deploy:**

1. Push your code and models to GitHub (using Git LFS for large files).
2. Connect your repo to Render and deploy using the provided `render.yaml`.

---

## Project Structure

```
breast_cancer/
├── app.py                  # FastAPI backend
├── build.sh                # Build script for Render
├── render.yaml             # Render deployment config
├── requirements.txt        # Python dependencies
├── frontend/               # React frontend (Vite)
│   ├── public/             # Static assets & sample CSVs
│   └── src/                # React components & styles
├── *.joblib                # ML model files (tracked with Git LFS)
├── *.json                  # Model summaries, config
└── ...                     # Data, scripts, notebooks, etc.
```

---

## Model Information

- **Targets:** Malignancy, vital status, cancer type, stage, metastasis, treatment outcome, treatment type, clinical trial, age at index, tumor classification, disease response, tissue/organ of origin, and more.
- **Techniques:** Random Forest, Gradient Boosting, Extra Trees, Voting Classifier, GridSearchCV, feature selection, and robust preprocessing.
- **Consistency Engine:** Ensures biologically plausible and logically consistent predictions across all targets.

---

## Usage Notes

- **Batch Upload:** Use the provided CSV templates in `frontend/public/` for correct formatting.
- **Model Files:** All `.joblib` model files must be present in the root directory for predictions to work.
- **Environment Variables:** See `render.yaml` for required variables (e.g., `PYTHON_VERSION`, `NODE_VERSION`).

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements, bug fixes, or new features.

---

## License

This project is licensed under the MIT License.

---

## Acknowledgments

- UCI Machine Learning Repository
- Render.com for cloud deployment
- [scikit-learn](https://scikit-learn.org/), [FastAPI](https://fastapi.tiangolo.com/), [React](https://react.dev/)

---

**For questions or support, please contact [herberzs70@gmail.com](mailto:herberzs70@gmail.com).**
