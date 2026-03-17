import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv('dataset/tmdb_5000_movies.csv')
credits = pd.read_csv('dataset/tmdb_5000_credits.csv')

movies = movies.merge(credits,on='title')

movies = movies[['movie_id','title','overview']]

movies.dropna(inplace=True)

cv = CountVectorizer(max_features=5000,stop_words='english')

vectors = cv.fit_transform(movies['overview']).toarray()

similarity = cosine_similarity(vectors)
#similarity = cosine_similarity(vectors)

pickle.dump(movies,open('movies.pkl','wb'))

from model import similarity

#pickle.dump(similarity,open('similarity.pkl','wb'))