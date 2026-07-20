# 🛡️ UAV Intrusion Detection System

A Flask-based web application for detecting cyber attacks in UAV network traffic using a tuned XGBoost machine learning model.

## 🚀 Features

- Multi-class UAV intrusion detection
- Tuned XGBoost model (~95.15% test accuracy)
- CSV file upload support
- Prediction history
- Dashboard with statistics
- PostgreSQL database integration
- Flask backend with modular architecture

## 🧠 Machine Learning

Model: Tuned XGBoost

Detected Classes:

- Normal Traffic
- Blackhole Attack
- Flooding Attack
- Sybil Attack
- Wormhole Attack

Test Accuracy:

95.15%

## 🛠 Tech Stack

Backend

- Flask
- Flask SQLAlchemy
- Flask Migrate

Machine Learning

- XGBoost
- Scikit-learn
- Pandas
- Joblib

Database

- PostgreSQL

Frontend

- HTML
- CSS
- JavaScript

## 📂 Project Structure

```
app/
├── ml_models/
├── models/
├── routes/
├── services/
├── static/
└── templates/

migrations/
run.py
requirements.txt
```

## ⚙️ Installation

```bash
git clone https://github.com/dhirj-ngm/uav-intrusion-detection-system.git

cd uav-intrusion-detection-system

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python run.py
```

## 👨‍💻 Author

Dheeraj Nigam
