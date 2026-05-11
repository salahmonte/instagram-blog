from django import forms 
from .models import Post

class PostForm (forms.modelform):
 class meta:
    model = Post
    fields = {'title','body','category','img'}