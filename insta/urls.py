from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path



urlpatterns = [
    path('', views.home, name='instahome'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('category/', views.category, name='category'),
    path('postDetails/<int:pk>/', views.postDetails, name='postDetails'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('createpost/', views.CreatePost, name='create_post'),
    path('edit/<int:pk>/', views.edit_post, name='edit_post'),
    path('delete/<int:pk>/', views.delete_post, name='delete_post'),
    path('allposts/', views.all_posts, name='all_posts'),
    
]
    
