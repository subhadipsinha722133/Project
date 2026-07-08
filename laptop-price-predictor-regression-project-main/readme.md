
---

# 🧠💻 **Laptop Price Predictor**

> 🚀 *An AI-powered web app that predicts laptop prices using advanced machine learning and ensemble techniques.*

<p align="center">
  <img src="https://github.com/yourusername/laptop-price-predictor/assets/banner.png" alt="Laptop Price Predictor Banner" width="80%">
</p>

---

### 🏷️ **Tech Stack Badges**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge\&logo=streamlit\&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge\&logo=scikitlearn\&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge\&logo=pandas\&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-EB5E0B?style=for-the-badge\&logo=xgboost\&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge\&logo=plotly\&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge\&logo=numpy\&logoColor=white)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-FF6F00?style=for-the-badge\&logo=TensorFlow\&logoColor=white)

---

## 🌐 **Live Demo**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

---

## 📚 **Table of Contents**

* [✨ Features](#-features)
* [🎥 Demo](#-demo)
* [🛠️ Installation](#️-installation)
* [🎯 Usage](#-usage)
* [📁 Project Structure](#-project-structure)
* [🤖 Model Details](#-model-details)
* [📊 API Documentation](#-api-documentation)
* [🎨 Customization](#-customization)
* [🤝 Contributing](#-contributing)
* [📈 Future Enhancements](#-future-enhancements)
* [🏆 Acknowledgments](#-acknowledgments)
* [📄 License](#-license)
* [📞 Support](#-support)
* [🔗 Links](#-links)

---

## ✨ **Features**

### 🎯 Core Highlights

* 💰 **Smart Price Prediction** — Accurate ML-based estimation
* ⚡ **Real-Time Analysis** — Instant interactive predictions
* 🧠 **Feature-Rich Model** — 12+ laptop parameters used
* 💹 **Market Insights** — Price comparisons & recommendations

### 📊 Visualization

* 📈 **Interactive Charts** — View trends and price distributions
* 🧩 **Feature Impact** — See which factors affect prices most
* 💡 **Market Comparison** — Brand and spec-wise analysis

### 💡 Smart Capabilities

* 🪙 **Price Categorization** — Budget, Mid-Range, High-End, Premium
* 🧭 **Optimization Tips** — Get better price-performance ratios
* 🧠 **Trend Insights** — Understand current market behaviors

---

## 🎥 **Demo**

### ⚙️ Quick Prediction Steps

1️⃣ **Select Specifications** → Choose brand, RAM, storage, CPU, etc.
2️⃣ **Get Prediction** → Instantly see estimated price
3️⃣ **Review Insights** → Market comparison and recommendations

<p align="center">
  <img src="demo/demo.gif" width="70%" alt="Demo Preview">
</p>

---

## 🛠️ **Installation**

### 🔧 Prerequisites

* 🐍 Python 3.8+
* 📦 pip installed

### 🚀 Setup Guide

```bash
# 1️⃣ Clone Repository
git clone https://github.com/yourusername/laptop-price-predictor.git
cd laptop-price-predictor

# 2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows

# 3️⃣ Install Dependencies
pip install -r requirements.txt

# 4️⃣ Train Model
python main.py

# 5️⃣ Launch Web App
streamlit run app.py
```

---

## 📁 **Project Structure**

```
laptop-price-predictor/
│
├── app.py               # 🖥️ Streamlit Web 
├── main.py              # 🧠 Model Training Script
├── requirements.txt     # 📦 Dependencies
├── laptop_data.csv      # 📊 Raw Dataset
├── df.pkl               # 🧾 Processed Data
├── pipe.pkl             # 🤖 Trained Model
├── laptop-price-predictor.ipynb
```

---

## 🎯 **Usage**

### 🧠 Train Model

```bash
python main.py
```

🧹 Cleans & preprocesses data
⚙️ Performs feature engineering
🏗️ Trains multiple models
🏆 Saves best model as `pipe.pkl`

### 🌍 Run App

```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser 🌐

### 💬 Predict Laptop Price

Choose:

* 🏷️ Brand (Dell, Lenovo, Apple)
* 💾 RAM / Storage
* ⚙️ CPU / GPU
* 🪶 Weight / Display Type
* 💻 OS

➡️ Get instant price prediction and comparison 📊

---

## 🤖 **Model Details**

### 🧩 Techniques Used

* 🧠 **Ensemble Learning** – Multiple ML models for higher accuracy
* 🧮 **Feature Engineering** – Derived PPI, Display, and Performance features
* ⚙️ **Hyperparameter Tuning** – Grid and Randomized Search

### 📈 Performance Metrics

| Metric      | Score       |
| ----------- | ----------- |
| 🧮 R² Score | 0.85 – 0.92 |
| 🎯 MAE      | $80 – $120  |
| ⚡ Accuracy  | 85% – 92%   |

### 💻 Features Used

| Category        | Features               |
| --------------- | ---------------------- |
| **Basic**       | Brand, Type, Weight    |
| **Performance** | RAM, CPU, GPU, Storage |
| **Display**     | PPI, Touchscreen, IPS  |
| **Software**    | Operating System       |

---

## 📊 **API Documentation**

### 🧠 Prediction Endpoint

```python
specifications = {
    "Company": "Dell",
    "TypeName": "Gaming",
    "Ram": 16,
    "Weight": 2.5,
    "Touchscreen": 0,
    "Ips": 1,
    "ppi": 180,
    "Cpu brand": "Intel Core i7",
    "HDD": 0,
    "SSD": 512,
    "Gpu brand": "Nvidia",
    "os": "Windows"
}

# Output
{
    "predicted_price": 1299.99,
    "price_category": "High-End",
    "confidence": 0.89
}
```

---

## 🎨 **Customization**

### 🧱 Add New Features

1️⃣ Modify `main.py` for feature engineering
2️⃣ Update `app.py` for new inputs
3️⃣ Retrain & regenerate `pipe.pkl`

### 🧩 UI Styling

* Edit CSS in `app.py`
* Change color schemes 🌈
* Add Plotly/Altair charts for better visuals

---

## 🤝 **Contributing**

We ❤️ open-source contributions!

### 🔧 Developer Workflow

1. 🍴 Fork this repo
2. 🌿 Create a feature branch
3. 🛠️ Implement changes
4. ✅ Add tests
5. 🔁 Submit PR

🐛 Found an issue? Report it here 👉 [GitHub Issues](https://github.com/yourusername/laptop-price-predictor/issues)

---

## 📈 **Future Enhancements**

* 📱 Mobile App (Android/iOS)
* 🌐 RESTful API for developers
* 💾 Larger & updated dataset
* 📆 Historical price analysis
* 🌍 Multi-language UI
* 📤 Export reports as PDF/CSV

---

## 🏆 **Acknowledgments**

* 🧠 **ML Libraries** – Scikit-learn, XGBoost
* 🌐 **Web Framework** – Streamlit
* 📊 **Visualization** – Plotly, Matplotlib

---

## 📄 **License**

🪪 Licensed under the **MIT License** – see [LICENSE](LICENSE)

---

## 📞 **Support**


* 🐛 Issues → [GitHub Issues](https://github.com/yourusername/laptop-price-predictor/issues)
* 📧 Email → [sinhasubhadip34@gmail.com](sinhasubhadip34@gmail.com)

---

## 🔗 **Links**

🌍 **Live App:** [Streamlit Demo](https://your-app-url.streamlit.app)
💾 **Source Code:** [GitHub Repository](https://github.com/yourusername/laptop-price-predictor)


---
