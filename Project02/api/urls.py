from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingPage),
    path('getUsers/', views.getUsers),
    path('signup/', views.signup),
    path('login/', views.login),
    path('logout/', views.logout),
    path('deleteAccount/', views.deleteAccount),
    path('createUser/', views.createUser),
    path('deleteUser/', views.deleteUser),
    path('updateUser/', views.updateUser),
]