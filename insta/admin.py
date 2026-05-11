from django.contrib import admin
from .models import Post, Categorie  # Correct import (capitalized)

admin.site.register(Post)
admin.site.register(Categorie)