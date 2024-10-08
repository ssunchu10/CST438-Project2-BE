from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
from rest_framework import generics
from projectApp.models import User, Item, List
from .serializers import UserSerializer, ItemSerializer
from rest_framework.views import APIView

# Show all users 
@api_view(['GET'])
def getUsers(request):
    # Grab all of the Users
    users = User.objects.all()
    # Serialize and return all Users
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# Create a user using POST method
@api_view(['POST'])
def createUser(request):
    # Grab email and password from user input
    email = request.data.get('email')
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')

    # Check if email already exists 
    if(User.objects.filter(email=email).exists()):
        return Response({'error': 'User with this email already exists.'}, status=400)

    if(password != confirm_password):
        return Response({'error': 'Passwords do not match.'}, status=400)
    
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
            user = User.objects.get(id=user_id)  # Retrieve user object by ID
            del request.session['user_id']  # Remove user_id from the session
            
            return Response({
                'message': f'Successfully logged out!',
                'user': {
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
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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