# 🛡️ UAV Intrusion Detection System

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask)
![XGBoost](https://img.shields.io/badge/XGBoost-ML%20Model-orange)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?logo=postgresql)
![Railway](https://img.shields.io/badge/Deployment-Railway-purple)
![License](https://img.shields.io/badge/License-MIT-green)

</p>

---

## 🌐 Live Demo

**Application:** https://uav-intrusion-detection-system-production.up.railway.app

---

# 📖 Overview

The **UAV Intrusion Detection System** is a machine learning-powered web application designed to identify malicious activities within Unmanned Aerial Vehicle (UAV) communication networks.

The application enables users to upload UAV network traffic datasets, perform real-time intrusion detection using a tuned **XGBoost classifier**, visualize prediction results, and store historical analyses in a PostgreSQL database.

The project demonstrates an end-to-end machine learning deployment workflow, from model development and inference to cloud deployment and database integration.

---

# 🎯 Why This Project?

With the rapid adoption of UAVs in defense, logistics, agriculture, surveillance, and emergency response, securing aerial communication networks has become increasingly important.

This project explores how machine learning can be applied to detect malicious traffic patterns in UAV communication systems through a complete production-style web application.

Rather than focusing solely on model accuracy, this project emphasizes the full deployment lifecycle including backend development, cloud deployment, database integration, and interactive visualization.

---

# ✨ Features

- Upload UAV network traffic datasets (.csv)
- Real-time attack prediction using XGBoost
- Detection of five traffic categories
- Interactive dashboard
- Prediction history storage
- PostgreSQL database integration
- Cloud deployment on Railway
- Modular Flask application architecture

---

# 🛠️ Technology Stack

## Backend

- Python
- Flask
- Flask SQLAlchemy
- Flask Migrate

## Machine Learning

- XGBoost
- Scikit-learn
- Pandas
- Joblib

## Database

- PostgreSQL
- Neon Database

## Deployment

- Railway
- Gunicorn

## Version Control

- Git
- GitHub

---

# 🧠 Machine Learning Pipeline

```
CSV Dataset
      │
      ▼
Upload & Validation
      │
      ▼
Feature Selection
      │
      ▼
Tuned XGBoost Classifier
      │
      ▼
Prediction Generation
      │
      ├────────────► Dashboard
      │
      └────────────► PostgreSQL Database
                          │
                          ▼
                 History & Analytics
```

---

# 🏗️ Project Architecture

```
app/
│
├── ml_models/
│
├── models/
│
├── routes/
│
├── services/
│
├── static/
│
├── templates/
│
├── config.py
│
└── __init__.py

migrations/

run.py

requirements.txt
```

---

# 📊 Model Performance

| Metric | Value |
|---------|--------|
| Algorithm | Tuned XGBoost |
| Training Accuracy | 96.29% |
| Testing Accuracy | 95.15% |
| Classes | 5 |
| Dataset Size | 122,171 Samples |

### Prediction Classes

- Normal Traffic
- Flooding Attack
- Sybil Attack
- Blackhole Attack
- Wormhole Attack

---

# 📂 Dataset Information

The dataset contains UAV network traffic records representing both legitimate communication and multiple intrusion scenarios.

Each record is processed through feature selection before being passed into the trained XGBoost classifier for prediction.

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/dhirj-ngm/uav-intrusion-detection-system.git
```

Move into the project

```bash
cd uav-intrusion-detection-system
```

Install dependencies

```bash
pip install -r requirements.txt
```

Configure environment variables

```env
DATABASE_URL=
SECRET_KEY=
MODEL_PATH=
FLASK_ENV=
```

Run database migrations

```bash
flask db upgrade
```

Start the application

```bash
python run.py
```

---

# 🌍 Deployment

This application is deployed using:

- Railway
- Neon PostgreSQL
- Gunicorn

---

# 🔮 Future Improvements

- Live UAV packet monitoring
- REST API endpoints
- Docker support
- JWT Authentication
- User login system
- SHAP Explainability
- Feature Importance visualization
- Confusion Matrix visualization
- Automatic model retraining
- CI/CD using GitHub Actions

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Dheeraj Nigam**

---

⭐ If you found this project interesting, consider giving it a star.