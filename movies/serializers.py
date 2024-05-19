from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Movie, Genre, Review


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('genre_id', 'name')

class MovieListSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        exclude = ('embedding',)

    def get_genres(self, obj):
      return GenreSerializer(obj.genres.all(), many=True).data


class MovieSerializer(serializers.ModelSerializer):
  genres = serializers.SerializerMethodField()

  class LikeUserListSerializer(serializers.ModelSerializer):
     class Meta:
        model = get_user_model()
        fields = ('pk', 'username')

  like_users = LikeUserListSerializer(many=True, read_only=True)

  class Meta:
    model = Movie
    fields = '__all__'

  def get_genres(self, obj):
    return GenreSerializer(obj.genres.all(), many=True).data

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'movie')

class GenreListSerializer(serializers.ModelSerializer):
  class Meta:
    model = Genre
    fields = '__all__'
