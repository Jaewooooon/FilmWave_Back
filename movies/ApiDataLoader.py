import requests
from django.conf import settings
from .models import Movie, Genre
# Create your views here.
api_key = settings.TMDB_API_KEY

def load_movie_data():
  print('loaddata')

  headers = {
    'accept': 'application/json',
    'Authorization': f'Bearer {api_key}'
  }


  for i in range(1, 250):
    # url = f'https://api.themoviedb.org/3/movie/popular?language=ko-KR&page={i}'
    url = f'https://api.themoviedb.org/3/discover/movie?include_video=false&language=ko-KR&page={i}&sort_by=popularity.desc'

    response = requests.get(url, headers=headers).json()

    movie_list = response["results"]

    for movie in movie_list:
      genre_ids = movie.get("genre_ids", [])
      movie_id = movie.get("id")
      adult = movie.get("adult", False)
      overview = movie.get("overview", "")
      popularity = movie.get("popularity", 0.0)
      backdrop_path = movie.get("backdrop_path", "")
      poster_path = movie.get("poster_path", "")
      title = movie.get("title", "")
      vote_average = movie.get("vote_average", 0.0)
      release_date = movie.get('release_date', "")

      if release_date == "":
        release_date = None
      
      # print(genre_ids)
      # print(adult)
      # print(overview)
      # print(backdrop_path)
      # print(poster_path)
      # print(movie_id)
      # print(title)
      # print(vote_average)
      # print(release_date)
      # print(runtime)

      movie_instance, created = Movie.objects.update_or_create(
          movie_id=movie_id,
          defaults={
              'title': title,
              'overview': overview,
              'poster_path': poster_path,
              'popularity': popularity,
              'backdrop_path': backdrop_path,
              'release_date': release_date,
              'vote_average': vote_average,
              'adult': adult,
          }
      )

      # Genre 연결
      for genre_id in genre_ids:
          genre = Genre.objects.get(genre_id=genre_id)
          movie_instance.genres.add(genre)
  
  print('finish')


def load_genres():
  url = 'https://api.themoviedb.org/3/genre/movie/list?language=ko'

  headers = {
    'accept': 'application/json',
    'Authorization': f'Bearer {api_key}'
  }

  response = requests.get(url, headers=headers).json()

  genres = response.get('genres')
  for genre in genres:
    Genre.objects.get_or_create(genre_id=genre.get('id'), name=genre.get('name'))

def loadData(request):
  load_genres()
  load_movie_data()
  