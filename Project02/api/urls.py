from django.urls import path
from . import views
from .views import ListCreateAPIView

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
    path('items/', views.ItemList.as_view(), name='item-list'),  
    path('items/<int:item_id>/', views.ItemDetail.as_view(), name='item-detail'),
    path('lists/', ListCreateAPIView.as_view(), name='create-list'),
]