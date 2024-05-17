from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Movie
from .serializers import (
  MovieListSerializer
)


@api_view(['GET'])
def movie_list(request):
	movies = Movie.objects.order_by('-popularity')[:20]

	if request.method=="GET":
		serializer = MovieListSerializer(movies, many=True)
		return Response(serializer.data)
	