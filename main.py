from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from sklearn.decomposition import TruncatedSVD
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# LOAD DATA
# -------------------------
ratings = pd.read_csv("rating.csv")
anime = pd.read_csv("anime.csv")

# -------------------------
# CLEAN DATA
# -------------------------
ratings = ratings[ratings["rating"] != -1]
ratings = ratings.head(20000)

# -------------------------
# CREATE MATRIX
# -------------------------
matrix = ratings.pivot_table(
    index="user_id",
    columns="anime_id",
    values="rating"
).fillna(0)

# -------------------------
# SVD MODEL
# -------------------------
import pickle

with open("model.pkl", "rb") as f:
    pred_df = pickle.load(f)

print("✅ Backend ready")

# -------------------------
# IMAGE CACHE (IMPORTANT)
# -------------------------
image_cache = {}

def get_image(title):
    # use cache first
    if title in image_cache:
        return image_cache[title]

    try:
        res = requests.get(
            f"https://api.jikan.moe/v4/anime?q={title}&limit=1",
            timeout=3
        )
        data = res.json()

        if data.get("data"):
            img = data["data"][0]["images"]["jpg"]["image_url"]
            image_cache[title] = img
            return img

    except:
        pass

    # fallback
    fallback = "https://via.placeholder.com/300x400?text=Anime"
    image_cache[title] = fallback
    return fallback

# -------------------------
# ROUTES
# -------------------------
@app.get("/")
def home():
    return {"message": "Anime recommender running"}


@app.get("/recommend")
def recommend(user_id: int = 1, n: int = 6):

    # fallback user
    if user_id not in pred_df.index:
        user_id = pred_df.index[0]

    user_pred = pred_df.loc[user_id]

    watched = ratings[ratings["user_id"] == user_id]["anime_id"].values
    recommendations = user_pred.drop(watched, errors="ignore")

    top_ids = recommendations.sort_values(ascending=False).head(n).index

    result = []

    for anime_id in top_ids:
        row = anime[anime["anime_id"] == anime_id]

        if row.empty:
            continue

        row = row.iloc[0]

        title = str(row["name"]).split("(")[0].strip()
        genre = str(row["genre"]).split(",")[0]

        result.append({
            "title": title,
            "rating": float(user_pred[anime_id]),
            "genre": genre,
            "image": get_image(title)
        })

    return result