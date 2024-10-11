# api/models.py

from django.db import models
from django.db.models import Avg

class Movie(models.Model):
    title = models.CharField(max_length=255)

    @property
    def rating(self):
        average = self.ratings.aggregate(avg=Avg('value'))['avg']
        return round(average, 1) if average is not None else None

    def __str__(self):
        return self.title

class Rating(models.Model):
    movie = models.ForeignKey(Movie, related_name='ratings', on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return f"Rating {self.value} for {self.movie.title}"
