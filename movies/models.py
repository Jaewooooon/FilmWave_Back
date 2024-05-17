from django.db import models

# Create your models here.
class Movie(models.Model):
  movie_id = models.CharField(max_length=100, primary_key=True)
  title = models.TextField()
  overview = models.TextField()
  poster_path = models.TextField()
  poster_path = models.TextField()
  release_date = models.DateField()
  runtime = models.IntegerField()
  vote_average = models.FloatField()
  genres = models.ManyToManyField('Genre', related_name=movies)


class Genre(models.Model):
    name = models.CharField(max_length=50)
    