from django.urls import path
from . import views

urlpatterns = [
    path('', views.group_list),
    path('<int:group_id>/', views.group_detail),
    path('<int:group_id>/', views.group_detail),
    path('<int:group_id>/memberships/', views.membership_list),             
]
