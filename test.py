import requests
from flask import request

data = [1, 3, 6, 2, 0, 5, 23, 10, 7, 20]
all_movie = sorted(data, reverse=True)
# print(sort[0])
for movie in range(5):
    print(all_movie[movie])


# APIKEY = 'b9a47fe57ebbebfa92c6ca9a7eaf11c8'
# tmdb_url = f'https://api.themoviedb.org/3/search/movie?query=venom&api_key={APIKEY}'
# responce = requests.get(tmdb_url).json()
# print(responce)





from dotenv import load_dotenv
import os

# # Load the .env file
load_dotenv()
print(os.getenv("APIKEY"))
# # Now fetch the key
# APIKEY = os.getenv('APIKEY')
# # APIKEY = os.getenv()
#
# # APIKEY = 'b9a47fe57ebbebfa92c6ca9a7eaf11c8'
# tmdb_url = f'https://api.themoviedb.org/3/search/movie?query=venom&api_key={APIKEY}'
# responce = requests.get(tmdb_url).json()
# print(responce)
# # print(key)
# # print(os.environ)

