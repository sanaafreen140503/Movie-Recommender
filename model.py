import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
movies = pd.read_csv('dataset/tmdb_5000_movies.csv')

# Select required columns (FIXED: id instead of movie_id)
movies = movies[['id', 'title', 'overview']]

# Remove missing values
movies.dropna(inplace=True)

# Convert text into vectors
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['overview']).toarray()

# Compute similarity
similarity = cosine_similarity(vectors)

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    movie_ids = []

    for i in movie_list:
        movie_ids.append(movies.iloc[i[0]].id)   # FIXED
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies, movie_ids