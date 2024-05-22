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
        exclude = ('embedding', 'genre_embedding')

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
    exclude = ('embedding', 'genre_embedding')

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


class ReviewWithMovieSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('id', 'username',)

    movie = MovieListSerializer()
    user = UserSerializer()
    
    class Meta:
        model = Review
        fields = '__all__'