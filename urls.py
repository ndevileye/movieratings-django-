# api/urls.py

from django.urls import path
from .views import MovieListCreateView, MovieDetailView, RatingCreateView

urlpatterns = [
    path('movies/', MovieListCreateView.as_view(), name='movie-list-create'),
    path('movies/<int:id>/', MovieDetailView.as_view(), name='movie-detail'),
    path('ratings/', RatingCreateView.as_view(), name='rating-create'),
]
