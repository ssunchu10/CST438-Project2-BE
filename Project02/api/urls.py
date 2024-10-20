from django.urls import path
from . import views
from .views import ItemList, ItemDetail, ListCreateAPIView, ListDetailAPIView, UserListAPIView

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
    path('getAllItems/', ItemList.as_view(), name='get-all-items'), 
    path('items/<int:item_id>/', ItemDetail.as_view(), name='get-item'),  
    path('addItem/', views.add_item, name='add-item'),  
    path('items/<int:item_id>/delete/', views.delete_item, name='delete-item'),  
    path('items/<int:item_id>/update/', ItemDetail.as_view(), name='update-item'),  
    # List-related paths
    path('lists/<int:list_id>/', ListDetailAPIView.as_view(), name='get-list'), 
    path('user/<int:user_id>/lists/', UserListAPIView.as_view(), name='get-user-lists'),  
    path('createList/', ListCreateAPIView.as_view(), name='create-list'),
]