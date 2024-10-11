from django.shortcuts import render

# Create your views here.


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer
from django.shortcuts import get_object_or_404


class MovieListCreateView(APIView):
    """
    GET /movies/ - List all movies
    POST /movies/ - Create a new movie
    """

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            movie = Movie.objects.create(title=serializer.validated_data['title'])
            response_serializer = MovieSerializer(movie)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieDetailView(APIView):
    """
    GET /movies/<id>/ - Retrieve a movie by ID
    """

    def get(self, request, id):
        movie = get_object_or_404(Movie, id=id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RatingCreateView(APIView):
    """
    POST /ratings/ - Create a new rating
    """

    def post(self, request):
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            movie_id = serializer.validated_data['movie'].id
            try:
                movie = Movie.objects.get(id=movie_id)
            except Movie.DoesNotExist:
                return Response({'detail': 'Movie not found.'}, status=status.HTTP_404_NOT_FOUND)

            rating = Rating.objects.create(
                movie=movie,
                value=serializer.validated_data['value']
            )
            response_serializer = RatingSerializer(rating)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        # Check if the error is due to invalid movie
        if 'movie' in serializer.errors:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

        # Check if the error is due to invalid value
        if 'value' in serializer.errors:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
