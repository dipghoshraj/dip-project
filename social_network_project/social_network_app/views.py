from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, FriendRequestSerializer, FriendshipSerializer
from .models import FriendRequest, Friendship, User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.core.cache import cache



DEFAULT_RATE_LIMIT = 3
CACHE_TTL = 60


from django.core.exceptions import PermissionDenied
# Create your views here.
class UserSignup(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        email = request.data.get('email')
        password = request.data.get('password')
        user = serializer.authenticate(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({'token': str(refresh.access_token)}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

class UserSearchAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return User.objects.filter(Q(email__icontains=query) | Q(username__icontains=query))


class SendFriendRequestAPIView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        from_user = self.request.user
        to_user_id = request.data.get('to_user')

        user_identifier = self.request.user.email
        cache_key = f'rate_limit:{user_identifier}'
        request_count = cache.get(cache_key, 0)

        print(request_count, DEFAULT_RATE_LIMIT)
        if request_count >= DEFAULT_RATE_LIMIT:
            raise PermissionDenied("Rate limit exceeded.")
        cache.set(cache_key, request_count + 1, timeout=CACHE_TTL)


        try:
            to_user = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if from_user == to_user:
            return Response({"error": "You cannot send friend request to yourself"}, status=status.HTTP_400_BAD_REQUEST)

        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response({"error": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)

        if Friendship.objects.filter(Q(user1=from_user, user2=to_user) | Q(user1=to_user, user2=from_user)).exists():
            return Response({"error": "You are already friends"}, status=status.HTTP_400_BAD_REQUEST)

        friend_request = FriendRequest.objects.create(from_user=from_user, to_user=to_user)
        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AcceptFriendRequestAPIView(generics.UpdateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        friend_request_id = kwargs.get('pk')
        try:
            friend_request = FriendRequest.objects.get(id=friend_request_id, to_user=request.user)
        except FriendRequest.DoesNotExist:
            return Response({"error": "Friend request does not exist"}, status=status.HTTP_404_NOT_FOUND)

        friend_request.accepted = True
        friend_request.save()

        Friendship.objects.create(user1=friend_request.from_user, user2=friend_request.to_user)
        Friendship.objects.create(user1=friend_request.to_user, user2=friend_request.from_user)

        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data)

class RejectFriendRequestAPIView(generics.UpdateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        friend_request_id = kwargs.get('pk')
        try:
            friend_request = FriendRequest.objects.get(id=friend_request_id, to_user=request.user)
        except FriendRequest.DoesNotExist:
            return Response({"error": "Friend request does not exist"}, status=status.HTTP_404_NOT_FOUND)

        friend_request.rejected = True
        friend_request.save()

        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data)

class ListFriendsAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friendships = Friendship.objects.filter(user1=user) | Friendship.objects.filter(user2=user)
        friend_ids = [friendship.user1_id if friendship.user1_id != user.id else friendship.user2_id for friendship in friendships]
        return User.objects.filter(id__in=friend_ids)

class ListPendingFriendRequestsAPIView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, accepted=False, rejected=False)