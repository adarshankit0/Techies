from django.urls import path
from . import views

urlpatterns = [
    path('', views.codeHome, name='code-home'),
    path('problem/<str:pk>/', views.problemPage, name='problem'),
    path('leaderboard/', views.leaderboardPage, name='leaderboard'),   # ✅ FIXED
    path('myscore/', views.myScore, name='myscore'),
    path('certificate/', views.certificatePage, name='certificate'),
    path('certificate/download/<int:cert_id>/', views.downloadCertificate, name='download-cert'),
    path('dashboard/', views.dashboard, name="dashboard"),
]