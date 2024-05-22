from django.urls import path
from . import views

urlpatterns = [
    path('', views.group_list),
    path('my/', views.my_group_list),
    path('<int:group_id>/', views.group_detail),
    path('<int:group_id>/', views.group_detail),
    path('<int:group_id>/membership-requests/', views.membership_request_list),
    path('<int:group_id>/membership-requests/<int:membership_request_id>/', views.membership_request_detail),
    path('<int:group_id>/membership/', views.group_leave),
    path('<int:group_id>/movies/', views.group_like_movie_list),
    path('<int:group_id>/posts/', views.group_post_list),
    path('<int:group_id>/posts/<int:post_id>/', views.group_post_detail),
    path('<int:group_id>/posts/<int:post_id>/comments/', views.group_comment_list),
    path('<int:group_id>/posts/<int:post_id>/comments/<int:comment_id>/', views.group_comment_detail),
]
