from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.Registerview,name='register'),
    path('login/',views.LoginView,name="login"),
    path('logout/', views.LogoutView, name='logout')
]
