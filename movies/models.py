from django.db import models
from django.conf import settings

class Movie(models.Model):
  movie_id = models.CharField(max_length=100, primary_key=True)
  title = models.TextField()
  overview = models.TextField(null=True)
  popularity = models.FloatField(null=True)
  backdrop_path = models.TextField(null=True)
  poster_path = models.TextField(null=True)
  release_date = models.DateField(null=True)
  vote_average = models.FloatField(null=True)
  adult = models.BooleanField(default=False)
  genres = models.ManyToManyField('Genre', related_name="movies")
  like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_movies")

class Genre(models.Model):
    genre_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=50)

class Review(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
  content = models.CharField(max_length=250)
  score = models.FloatField()
