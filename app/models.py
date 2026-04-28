from django.db import models
from django.conf import settings
import uuid


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    uu_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    length = models.PositiveIntegerField(help_text="Movie duration in minutes")
    genre = models.ManyToManyField(Genre, related_name='movies', blank=True)
    image_card = models.ImageField(upload_to='cards/')
    image_banner = models.ImageField(upload_to='banners/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    movie_views = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def genre_names(self):
        return ", ".join([g.name for g in self.genre.all()])

    def __str__(self):
        return self.title


class MyList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"