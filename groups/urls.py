from django.urls import path
from . import views

urlpatterns = [
    path('', views.group_list),
    path('<int:group_id>/', views.group_detail),
    path('<int:group_id>/', views.group_detail),
    path('<int:group_id>/membership-requests/', views.membership_request_list),
    path('<int:group_id>/membership-requests/<int:membership_request_id>/', views.membership_request_detail),
]
