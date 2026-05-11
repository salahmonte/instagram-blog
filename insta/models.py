from django.db import models
import datetime
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class Categorie(models.Model):
    name = models.CharField(max_length=50, unique=True, default="general")
    def __str__(self):
        return self.name
    


# models.py
class Post(models.Model):
    STATUS = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    ]

    title = models.CharField(max_length=256)
    body = RichTextUploadingField()
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured = models.BooleanField(default=False)

    category = models.ForeignKey(Categorie, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='draft'
    )

    img = models.ImageField(
        upload_to='post',
        default='post/default.jpg',
        null=True
    )

    def __str__(self):
        return f'{self.title} by {self.author}'


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name  