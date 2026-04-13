from django.urls import path
from . import views

urlpatterns = [
    
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    
    
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),

    
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    
    path('update-user/', views.updateUser, name="update-user"),

    
    path('topics/', views.topicPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),

    
    path('ai/', views.aiPage, name="ai"),

    
    path('posts/', views.postsPage, name="posts"),

    
    path('add-friend/<str:user_id>/', views.sendFriendRequest, name="add-friend"),
    path('accept-friend/<str:request_id>/', views.acceptFriendRequest, name="accept-friend"),
    path('friends/', views.friendsPage, name="friends"),

    
    path('about/', views.aboutPage, name="about"),
    path('contact/', views.contactPage, name="contact"),
    path('help/', views.helpPage, name="help"),
    path('notifications/', views.notificationPage, name="notifications"),
]