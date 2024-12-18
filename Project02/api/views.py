from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
from rest_framework import generics, status
from projectApp.models import User, Item, List, Entry
from .serializers import UserSerializer, ItemSerializer, ListSerializer, EntrySerializer
from rest_framework.views import APIView
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from rest_framework.decorators import api_view, permission_classes
from .permissions import IsCustomAdmin
from django.shortcuts import get_object_or_404


#views.py
# ---------------- User Endpoints -------------
@api_view(['GET'])
def landingPage(request):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Landing Page</title>
    </head>
    <body>
        <h1>Welcome to Our Wishlist Website</h1>
        <p>This is the landing page of our app.</p>
    </body>
    </html>
    """
    return HttpResponse(html_content)

# User sign up using POST method
@api_view(['POST'])
def signup(request):
    # Grab email and password from user input
    email = request.data.get('email')
    password = request.data.get('password')

    # Check if email already exists 
    if(User.objects.filter(email=email).exists()):
        return Response({'error': 'User with this email already exists.'}, status=400)
    
    if(email == "admin@gmail.com"):
        return Response({'error': 'Cannot use admin email.'}, status=400)

    # Hash password before saving 
    hashed_password = make_password(password)

    # Prepare data
    data = {
        'email': email,
        'password': hashed_password
    }

    # Serialize data, check if it is valid 
    serializer = UserSerializer(data=data)

    # If all inputs match the restrictions (char limit) then save 
    if serializer.is_valid():
        user = serializer.save() 
        return Response({'data':serializer.data,'message': 'User successfully created.'},status=201)

    return Response(serializer.errors, status=400)

# Login Existing User
@api_view(['POST'])
def login(request):
    # Grab the email and password from input 
    email = request.data.get('email')
    password = request.data.get('password')

    # Check if user is in database 
    try:
        user= User.objects.get(email=email)
        print("the db password was", user.password)
        print("given was ", password)
        if(check_password(password, user.password)):
            # Serialize user
            serializer = UserSerializer(user)
            return Response({'data':serializer.data,'message': 'Successfully logged in!'},status=200)
        else: 
             return Response({'error': 'Invalid Password'}, status=400)

    except User.DoesNotExist:
         return Response({'error': 'User not found.'}, status=400)

# Logout Existing User
@api_view(['POST'])
def logout(request):
        # Get user object by ID to see who is logging out
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'User ID not provided.'}, status=400)
        try:
             # Grab user object by ID
            user = User.objects.get(id=user_id)
            return Response({
                'message': 'Successfully logged out!',
                'user': 
                {
                    'id': user.id,
                    'email': user.email,  
                }
            }, status=200)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=400)

# Update Logged In Account 
@api_view(['PATCH'])
def updateAccount(request):
    user_id = request.data.get('user_id')
    if not user_id:
        return Response({'error': 'User ID not provided.'}, status=400)
    try:
        user = User.objects.get(id=user_id)
        # Check which fields are being changed 
        if 'email' in request.data:
            user.email = request.data['email']
        if 'password' in request.data:
            user.password = make_password(request.data['password'])
        user.save()
        return Response({'message': 'User successfully updated.'}, status=200)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=404)


# Delete logged in account (confirm passsword should be done with frontend)
@api_view(['DELETE'])
def deleteAccount(request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        # Delete User
        user.delete()
        return Response({"message": "User deleted successfully"}, status=200)


#####################################
class ItemList(APIView):
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_item(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return Response({'message': 'Item deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

class ItemDetail(APIView):
    def get(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def patch(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)
        item.delete()
        return Response({'message': 'Item deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

# ---------------- List and Entry Endpoints -------------
class ListCreateAPIView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        request.data['user'] = user_id
        serializer = ListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListDetailAPIView(APIView):
    def get(self, request, list_id):
        list_instance = get_object_or_404(List, id=list_id)
        serializer = ListSerializer(list_instance)
        return Response(serializer.data)

class ListItems(APIView):
    def get(self, request, list_id):
        entries = Entry.objects.filter(list_id=list_id)
        if not entries.exists():
            return Response({'error': 'No items found for this list.'}, status=status.HTTP_404_NOT_FOUND)

        item_ids = entries.values_list('item_id', flat=True)
        items = Item.objects.filter(id__in=item_ids)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserListAPIView(APIView):
    def get(self, request, user_id):
        lists = List.objects.filter(user_id=user_id)
        serializer = ListSerializer(lists, many=True)
        return Response(serializer.data)

class AddEntryAPIView(APIView):
    def post(self, request, list_id):
        list_instance = get_object_or_404(List, id=list_id)
        item_id = request.data.get('item')

        item_instance = get_object_or_404(Item, id=item_id)

        entry_data = {
            'list': list_instance.id,
            'item': item_id
        }
        serializer = EntrySerializer(data=entry_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListItems(APIView):
    def get(self, request, list_id):
        entries = Entry.objects.filter(list_id=list_id)
        if not entries.exists():
            return Response({'error': 'No items found for this list.'}, status=status.HTTP_404_NOT_FOUND)

        item_ids = entries.values_list('item_id', flat=True)
        items = Item.objects.filter(id__in=item_ids)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ---------------- Admin Endpoints -------------
# Get Users Admin Function
@api_view(['GET'])
def getUsers(request):
    # Grab all of the Users
    users = User.objects.all()
    # Serialize and return all Users
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# Create Users Admin Function
@api_view(['PUT'])
def createUser(request):
    # Grab fields from admin input 
    email = request.data.get('email')
    password = request.data.get('password')
    is_admin = request.data.get('is_admin', False) #if is_admin not there it will default to false

    if User.objects.filter(email=email).exists():
        return Response({'error': 'User with this email already exists.'}, status=400)
    
    if email == "admin@gmail.com":
        return Response({'error': 'Cannot use admin email.'}, status=400)
    
    hashed_password = make_password(password)

    data = {
        'email':email,
        'password':hashed_password,
        'is_admin': is_admin
    }

    serializer = UserSerializer(data=data)
    # Check that the data is valid 
    if serializer.is_valid():
        user = serializer.save()
        return Response({'data': serializer.data, 'message': 'User successfully created.'}, status=201)
    # Error if not valid
    return Response(serializer.errors, status=400)  

# Delete User
@api_view(['DELETE'])
def deleteUser(request, user_id): 
    try:
        # Grab email object and delete
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({'message': f'User ID"{user_id}" successfully deleted.'}, status=204)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=404)
    
# Update User
@api_view(['PATCH'])
def updateUser(request, user_id):
    # Use email to identify account since emails are unique
    try:
        user = User.objects.get(id=user_id)
        # Check which fields are being changed 
        if 'email' in request.data:
            user.email = request.data['email']
        if 'password' in request.data:
            user.password = make_password(request.data['password'])
        if 'is_admin' in request.data:
            user.is_admin = request.data['is_admin']
        
        user.save()
        return Response({'message': 'User successfully updated.'}, status=200)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=404)

