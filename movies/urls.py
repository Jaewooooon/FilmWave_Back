from django.urls import path
from .ApiDataLoader import loadData
from . import views

urlpatterns = [
    path('api-data/', loadData),
    path('', views.movie_list),
    path('search/', views.movie_search),
    path('recommend/', views.movie_recommend_list),
    path('recent_reviewed/', views.movie_recent_review_list),
    path('<str:username>/likes/', views.movie_like_list),
    path('<str:username>/user-reviews/', views.user_review_list),
    path('<str:username>/likes/genre-frequency/', views.genre_frequency),
    path('<int:movie_id>/', views.movie_detail),
    path('<int:movie_id>/like/', views.movie_like),
    path('<int:movie_id>/reviews/', views.movie_review_list),
    path('<int:movie_id>/reviews/<int:review_id>/', views.movie_review_detail),
    path('genres/', views.genre_list),
]
