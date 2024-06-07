from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from .serializers import CustomUserSerializer,FriendRequestSerializer
from .models import CustomUser,Friend_Request
from rest_framework import status
from rest_framework.throttling import UserRateThrottle


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = CustomUser.objects.filter(email=email).first()
        if user is None:
            return Response({'error': 'User Not Found'}, status=status.HTTP_400_BAD_REQUEST)
        elif not user.check_password(password):
            return Response({'error': 'Invalid Password'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Login Successful'}, status=status.HTTP_200_OK)


#throttling,user rate limiting
class FriendRequestThrottle(UserRateThrottle):
    scope = 'friend-request'
    # rate = '3/min'
    def allow_request(self, request, view):
        if request.method == 'POST':
            return super().allow_request(request, view)
        return True



class FriendRequestView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [FriendRequestThrottle]
    
    def post(self,request):
        sent_to = CustomUser.objects.get(email=request.data.get('sent_to'))
        sent_by = request.user
        if sent_to == sent_by:
            return Response({'error': 'You cannot send request to yourself'}, status=status.HTTP_400_BAD_REQUEST)
        
        elif(Friend_Request.objects.filter(sent_to=sent_to, sent_by=sent_by).exists() or Friend_Request.objects.filter(sent_to=sent_by, sent_by=sent_to).exists()):
            return Response({'error': 'Friend Request Already Sent'}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            Friend_Request.objects.create(sent_to=sent_to, sent_by=sent_by)
            return Response({'message': 'Friend Request Sent'}, status=status.HTTP_201_CREATED)
    
    
    def get(self,request):
        pending_requests = Friend_Request.objects.filter(sent_to=request.user, status='pending')
        serializer = FriendRequestSerializer(pending_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
        
    def put(self, request):

        if(request.data.get('sent_by') != request.user.email):

            sent_by = CustomUser.objects.get(email=request.data.get('sent_by'))
            friend_request = Friend_Request.objects.filter(sent_by=sent_by, sent_to=request.user).first()  
           
            if friend_request:
                friend_request.status = 'accepted'
                friend_request.save()  # Save the individual object
                return Response({'message': 'Friend Request Accepted'}, status=status.HTTP_200_OK)
            return Response({'error': 'Friend Request Not Found'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error': 'You cannot accept this request'}, status=status.HTTP_400_BAD_REQUEST)

class FriendListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sent_friend_requests = Friend_Request.objects.filter(sent_by=request.user, status='accepted')
        received_friend_requests = Friend_Request.objects.filter(sent_to=request.user, status='accepted')

        friend_requests = sent_friend_requests | received_friend_requests

        serializer = FriendRequestSerializer(friend_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
class currentlyLoggedInUser(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class RejectFriendRequest(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self,request):
        if(request.data.get('sent_by') != request.user.email):

            sent_by = CustomUser.objects.get(email=request.data.get('sent_by'))
            friend_request = Friend_Request.objects.filter(sent_by=sent_by, sent_to=request.user).first()  
           
            if friend_request:

                if(friend_request.status == 'pending'):
                    friend_request.status = 'rejected'
                    friend_request.save()
                    return Response({'message': 'Friend Request Rejected'}, status=status.HTTP_200_OK)
                
                elif(friend_request.status == 'accepted'):
                    return Response({'error': 'You cannot reject an accepted request'}, status=status.HTTP_400_BAD_REQUEST)
                
                elif(friend_request.status == 'rejected'):
                    return Response({'error': 'You have already rejected this request'}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'error': 'Friend Request Not Found'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error': 'You cannot reject this request'}, status=status.HTTP_400_BAD_REQUEST)
    

class SearchUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        search_keyword = request.query_params.get('q','')

        if search_keyword:
            
            if '@' in search_keyword:
                user = CustomUser.objects.filter(email=search_keyword).first()
                if user:
                    serializer = CustomUserSerializer(user)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                users = CustomUser.objects.filter(name__icontains=search_keyword)
                serializer = CustomUserSerializer(users, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Please enter search keyword'}, status=status.HTTP_400_BAD_REQUEST)
    

        