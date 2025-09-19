from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

class Books(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.CharField(max_length=9999)
    price = models.IntegerField()
    image = models.ImageField(upload_to='book_images/', blank=True, null=True)
    published_date = models.DateField(blank=True, null=True)
    genres = models.TextField(blank=True, null=True, help_text='Comma-separated list of genres')
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True, related_name='books')

    def get_genre_list(self):
        return [g.strip() for g in self.genres.split(',')] if self.genres else []

    def get_genre_display(self):
        return ', '.join(self.get_genre_list())

    def average_rating(self):
        return self.reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0

    def __str__(self):
        return self.title

class Review(models.Model):
    rating = models.IntegerField()
    comment = models.TextField()
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='reviews', default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('book', 'user')