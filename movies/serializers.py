from rest_framework import serializers
from .models import Movie, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('genre_id', 'name')

class MovieListSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

    def get_genres(self, obj):
      return GenreSerializer(obj.genres.all(), many=True).data


class MovieSerializer(serializers.ModelSerializer):
  genres = serializers.SerializerMethodField()
  
  class Meta:
    model = Movie
    fields = '__all__'

  def get_genres(self, obj):
    return GenreSerializer(obj.genres.all(), many=True).data
  