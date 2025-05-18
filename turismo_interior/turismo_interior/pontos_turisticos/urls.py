from django.urls import path
from . import views

app_name = 'pontos_turisticos'

urlpatterns = [
    path('', views.TouristSpotListView.as_view(), name='spot-list'),
    path('statistics/', views.StatisticsView.as_view(), name='statistics'),
    path('api/types-for-city/', views.get_types_for_city, name='types_for_city'),
] 