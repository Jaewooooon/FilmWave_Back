from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.core.paginator import Paginator, EmptyPage

from .models import Movie, Review, Genre
from .serializers import (
  MovieSerializer,
  MovieListSerializer,
  ReviewSerializer,
  GenreListSerializer,
)

# 검색
import torch
import numpy as np
from .embedding import tokenizer, model


@api_view(['GET'])
def movie_list(request):
  if request.method=="GET":
    genreId = request.GET.get('genreId')
    page = request.GET.get('page', 1)

    if genreId:
      genre = get_object_or_404(Genre, pk=genreId)
      movies = genre.movies.all().order_by('-popularity')
    else: 
      movies = Movie.objects.order_by('-popularity')

    paginator = Paginator(movies, 20)

    try:
        page_obj = paginator.page(page)
    except EmptyPage:
        return Response({"detail": "없는 페이지입니다."}, status=status.HTTP_404_NOT_FOUND)
        

    serializer = MovieListSerializer(page_obj, many=True)
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


@api_view(['GET'])
def genre_list(request):
  if request.method=="GET":
    genres = get_list_or_404(Genre)
    serializer = GenreListSerializer(genres, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def movie_search(request):
    query = request.GET.get('q')
    print(query)
    if not query:
        return Response({'detail': 'Query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

    # 검색어 토크나이저
    query_tokens = tokenizer(query, return_tensors='pt', truncation=True, padding=True)

    # 검색어 임베딩 생성
    with torch.no_grad():
        query_embedding = model(**query_tokens).last_hidden_state.mean(dim=1)

    print('Query embedding completed')

    # 영화 제목 가져오기
    movies = Movie.objects.order_by('-popularity')
    movie_ids = [movie.pk for movie in movies]
    movie_titles = [movie.title for movie in movies]

    # 미리 계산된 임베딩 벡터를 하나의 텐서 만들기
    movie_embeddings = [torch.tensor(movie.embedding) for movie in movies]

    movie_embeddings = torch.stack(movie_embeddings)
    # 두 텐서간 코사인 유사도 계산 -> 텐서를 numpy 배열로 반환
    similarities = torch.nn.functional.cosine_similarity(query_embedding, movie_embeddings).numpy()

    # 검색어를 포함하고 있으면 유사도 증가 보정
    exact_match_bonus = 1.0 
    for idx, title in enumerate(movie_titles):
        if query.lower() in title.lower():
            similarities[idx] += exact_match_bonus

    sorted_indices = np.argsort(similarities)[::-1]

    # 유사도 순으로 영화 정렬
    sorted_movies = [movies[int(i)] for i in sorted_indices if similarities[int(i)] > 0]

    # 유사도 순으로 영화 정렬 (유사도와 함께)
    sorted_movies_with_similarity = [(movies[int(i)], similarities[int(i)]) for i in sorted_indices if similarities[int(i)] > 0]

    idx = 0
    for movie, similarity in sorted_movies_with_similarity:
        idx += 1
        if idx == 100:
           break
        print(f'Movie: {movie.title}, Similarity: {similarity}')

    serializer = MovieListSerializer(sorted_movies[:20], many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
