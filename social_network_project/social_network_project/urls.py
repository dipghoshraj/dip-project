"""
URL configuration for social_network_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]


from django.urls import path
from social_network_app.views import *

# urlpatterns = [
#     path('users/search/', UserSearchAPIView.as_view(), name='user_search'),
#     path('friend-request/send/', SendFriendRequestAPIView.as_view(), name='send_friend_request'),
#     path('friend-request/accept-reject/<int:pk>/', AcceptRejectFriendRequestAPIView.as_view(), name='accept_reject_friend_request'),
#     path('friends/', FriendListAPIView.as_view(), name='friend_list'),
#     path('friend-request/pending/', PendingFriendRequestsAPIView.as_view(), name='pending_friend_requests'),
# ]


urlpatterns = [
    path('signup/', UserSignup.as_view(), name='signup'),
    path('login/', UserLogin.as_view(), name='login'),
    path('users/search/', UserSearchAPIView.as_view(), name='user-search'),
    path('friend-requests/', SendFriendRequestAPIView.as_view(), name='friend-request-create'),
    path('friend-requests/<int:pk>/', AcceptFriendRequestAPIView.as_view(), name='friend-request-accept-reject'),
    path('friends/', ListFriendsAPIView.as_view(), name='friend-list'),
    path('pending-friend-requests/', ListPendingFriendRequestsAPIView.as_view(), name='pending-friend-requests-list'),
    path('reject-friend-requests/<int:pk>/', RejectFriendRequestAPIView.as_view(), name='pending-friend-requests-list'),
]



