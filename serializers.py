

from rest_framework import serializers
from .models import Movie, Rating

class MovieSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'rating']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'movie', 'value']

    def validate_value(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating value must be between 1 and 5.")
        return value

    def validate_movie(self, value):
        if not Movie.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Movie with the given ID does not exist.")
        return value
