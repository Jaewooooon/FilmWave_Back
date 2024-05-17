from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Movie, Review
from .serializers import (
	MovieSerializer,
	MovieListSerializer,
	ReviewSerializer,
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

@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def movie_like(request, movie_id):
	movie = get_object_or_404(Movie, pk=movie_id)

	if request.method=="POST":
		movie.like_users.add(request.user)
		serializer = MovieSerializer(movie)
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	elif request.method=="DELETE":
		movie.like_users.remove(request.user)
		serializer = MovieSerializer(movie)
		return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def movie_review_list(request, movie_id):
	movie = get_object_or_404(Movie, pk=movie_id)

	if request.method=="GET":
		reviews = movie.review_set.all()
		serializer = ReviewSerializer(reviews, many=True)
		return Response(serializer.data, status=status.HTTP_201_CREATED)

	elif request.method=="POST":
		serializer = ReviewSerializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			serializer.save(user=request.user, movie=movie)
			return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def movie_review_detail(request, movie_id, review_id):
	if request.method=="DELETE":
		review = get_object_or_404(Review, pk=review_id)
		if request.user == review.user:
			review.delete()
			return Response({'리뷰가 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
