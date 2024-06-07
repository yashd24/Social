from django.urls import path
from .views import RegistrationView,LoginView,FriendListView,FriendRequestView,currentlyLoggedInUser,RejectFriendRequest,SearchUser
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('friend-request/', FriendRequestView.as_view(), name='friend_request'),
    path('friend-request/friends/', FriendListView.as_view(), name='friends-list'),
    path('current-user/', currentlyLoggedInUser.as_view(), name='current-user'),
    path('friend-request/reject/', RejectFriendRequest.as_view(), name='reject-friend-request'),
    path('search-user/', SearchUser.as_view(), name='search-user'),

]

