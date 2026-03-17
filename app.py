import streamlit as st
import requests
import concurrent.futures
import os
from dotenv import load_dotenv
from model import movies, recommend   # ✅ IMPORT FROM MODEL

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("TMDB_API_KEY")

# Page config
st.set_page_config(page_title="Movie Recommender", layout="wide")

# ----------------------------
# Fetch Poster Function
# ----------------------------
@st.cache_data
def fetch_poster(movie_id):
    try:
        if not api_key:
            return "https://via.placeholder.com/500x750?text=No+API+Key"

        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            poster_path = data.get("poster_path")

            if poster_path:
                return "https://image.tmdb.org/t/p/w342" + poster_path

        return "https://via.placeholder.com/500x750?text=No+Poster"

    except:
        return "https://via.placeholder.com/500x750?text=Error"

# ----------------------------
# UI
# ----------------------------
st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button("Recommend"):

    with st.spinner("Loading recommendations... 🎬"):
        names, movie_ids = recommend(selected_movie)

        # Fetch posters in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            posters = list(executor.map(fetch_poster, movie_ids))

    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]

    for i in range(5):
        with cols[i]:
            st.image(posters[i], width=200)
            st.caption(names[i])