from django.urls import path
from . import views

urlpatterns = [
    path('', views.getUsers),
    path('signup/', views.createUser),
    path('login/', views.login),
    path('logout/', views.logout)
]