from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
from rest_framework import generics
from projectApp.models import User, Item, List
from .serializers import UserSerializer, ItemSerializer, ListSerializer
from rest_framework.views import APIView
from rest_framework import status
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer
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
        if(check_password(password, user.password)):
            # Save user ID and start a session
            request.session['user_id'] = user.id 

            # Check if admin email 
            # if(email == 'admin@gmail.com'):
            #     return adminLogin(request)

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
    #Logout by deleting the session of the current user_id 
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        # Get user object by ID to see who is logging out
        
        try:
             # Grab user object by ID
            user = User.objects.get(id=user_id)
             # Remove user_id from the session  
            del request.session['user_id']  
            
            return Response({
                'message': f'Successfully logged out!',
                'user': 
                {
                    'id': user.id,
                    'email': user.email,  
                }
            }, status=200)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=400)
    else:
        return Response({'error': 'No user is logged in.'}, status=400)


class ItemList(APIView):
    def get(self, request):
        list_id = request.query_params.get('list')
        user_id = request.query_params.get('user')
        item_id = request.query_params.get('itemID')
        if list_id:
            try:
                item_list = List.objects.get(id=list_id)
                if item_list.is_public:
                    items = Item.objects.filter(list_id=item_list.id)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            except List.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        elif user_id:
            if 'user_id' in request.session and request.session['user_id'] == int(user_id):
                items = Item.objects.filter(list__user_id=user_id)
            else:
                return Response({'error': 'User not logged in.'}, status=status.HTTP_401_UNAUTHORIZED)
        elif item_id:
            item = get_object_or_404(Item, id=item_id)
            serializer = ItemSerializer(item)
            return Response(serializer.data)

        else:
            items = Item.objects.all()

        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        list_id = request.data.get('list_id')
        try:
            list_obj = List.objects.get(id=list_id)  
        except List.DoesNotExist:
            return Response({'error': f'List with id {list_id} does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class ListCreateAPIView(APIView):
    def post(self, request):
        if('user_id' not in request.session):
            return Response({'error': 'User not logged in.'}, status=status.HTTP_401_UNAUTHORIZED)
        request.data['user'] = request.session['user_id']
        serializer = ListSerializer(data=request.data)

        if(serializer.is_valid()):
            list_instance = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
# Delete logged in account (is it okay to have delete as post? since we need to confirm the password)
@api_view(['POST'])
def deleteAccount(request):
    # Grab password from
    password = request.data.get('password')
    if 'user_id' in request.session:
        user_id = request.session['user_id']
    else:
        return Response({'error': 'No user is logged in.'}, status=400)
    try:
        # Grab user object by ID
        user = User.objects.get(id=user_id)
        # Password Confirmation before Deletion
        if(check_password(password, user.password)):
            # Delete User
            user.delete()
            # Clear the session
            request.session.flush() 
            return Response({"message": "User deleted successfully"}, status=200)
        else:
            return Response({"error": "Incorrect password"}, status=400)
    except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=400)


# ---------------- Admin Endpoints -------------
# Get Users Admin Function
@api_view(['GET'])
@permission_classes([IsCustomAdmin]) # Permission to check if they are an admin 
def getUsers(request):
    # Grab all of the Users
    users = User.objects.all()
    # Serialize and return all Users
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# Create Users Admin Function
@api_view(['PUT'])
@permission_classes([IsCustomAdmin]) # Permission to check if they are an admin 
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
@permission_classes([IsCustomAdmin])
def deleteUser(request):
    # Use email to identify account
    email = request.query_params.get('email')  
    try:
        # Grab email object and delete
        user = User.objects.get(email=email)
        user.delete()
        return Response({'message': f'User "{email}" successfully deleted.'}, status=204)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=404)
    
# Update User
@api_view(['PATCH'])
@permission_classes([IsCustomAdmin])
def updateUser(request):
    # Use email to identify account since emails are unique
    email = request.query_params.get('email') 

    try:
        user = User.objects.get(email=email)

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

