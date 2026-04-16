from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import requests
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# LOAD DATA (LIGHT)
# -------------------------
anime = pd.read_csv("anime.csv")

print("✅ Backend ready")

# -------------------------
# IMAGE CACHE
# -------------------------
image_cache = {}

def get_image(title):
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
def recommend(n: int = 6):

    sample = anime.sample(n * 3)

    result = []

    for _, row in sample.iterrows():
        title = str(row["name"]).split("(")[0].strip()
        genre = str(row["genre"]).split(",")[0]

        # ❌ FILTER BAD CONTENT
        if genre.lower() == "hentai":
            continue

        result.append({
            "title": title,
            "rating": round(random.uniform(2.0, 5.0), 1),
            "genre": genre,
            "image": get_image(title)
        })

        if len(result) == n:
            break

    return result