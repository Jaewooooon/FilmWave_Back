from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Movie
from .serializers import (
	MovieSerializer,
	MovieListSerializer,
)


@api_view(['GET'])
def movie_list(request):
	movies = Movie.objects.order_by('-popularity')[:20]

	if request.method=="GET":
		serializer = MovieListSerializer(movies, many=True)
		return Response(serializer.data)


@api_view(['GET'])
def movie_detail(request, movie_id):
	movie = get_object_or_404(Movie, pk=movie_id)

	if request.method=="GET":
		serializer = MovieSerializer(movie)
		return Response(serializer.data)