# 🎬 Anime Recommendation System

A full-stack anime recommendation system that suggests anime based on user preferences using Machine Learning.

---

## 🚀 Features

- Personalized anime recommendations
- Machine Learning model (SVD)
- Real anime posters via API
- FastAPI backend
- React frontend

---

## 🧠 How It Works

1. User enters a User ID
2. Backend analyzes rating data
3. SVD predicts unseen anime
4. System returns recommendations
5. Images are fetched dynamically

---

## 🛠️ Tech Stack

### Backend
- FastAPI
- Pandas
- Scikit-learn
- Requests

### Frontend
- React
- Tailwind CSS

---

## 🔗 API Example

GET /recommend?user_id=1

---

## ⚙️ Run Locally

### Backend
```bash
pip install -r requirements.txt
python main.py