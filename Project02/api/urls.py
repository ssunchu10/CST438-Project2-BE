from django.urls import path
from . import views
from .views import ItemList, ItemDetail, ListCreateAPIView, ListDetailAPIView, UserListAPIView, AddEntryAPIView, ListItems, deleteAccount

urlpatterns = [
    path('', views.landingPage),
    #user and admin paths
    path('getUsers/', views.getUsers),
    path('signup/', views.signup),
    path('login/', views.login),
    path('logout/', views.logout),
    path('deleteAccount/<int:user_id>/', deleteAccount, name='delete-account'),
    path('updateAccount/', views.updateAccount),
    path('createUser/', views.createUser),
    path('deleteUser/', views.deleteUser),
    path('updateUser/', views.updateUser),
    #item paths
    path('getAllItems/', ItemList.as_view(), name='get-all-items'), 
    path('items/<int:item_id>/', ItemDetail.as_view(), name='get-item'),  
    path('addItem/', views.add_item, name='add-item'),  
    path('items/<int:item_id>/delete/', views.delete_item, name='delete-item'),  
    path('items/<int:item_id>/update/', ItemDetail.as_view(), name='update-item'),  
    # List-related paths
    path('lists/<int:list_id>/', ListDetailAPIView.as_view(), name='get-list'), 
    path('user/<int:user_id>/lists/', UserListAPIView.as_view(), name='get-user-lists'),  
    path('createList/', ListCreateAPIView.as_view(), name='create-list'),
    path('lists/<int:list_id>/addEntry/', AddEntryAPIView.as_view(), name='add-entry'),  
    path('lists/<int:list_id>/items/', ListItems.as_view(), name='list-items'),
]