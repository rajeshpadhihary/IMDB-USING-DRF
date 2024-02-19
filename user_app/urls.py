from django.urls import path
from .views import Register_Users,login_user,User_logout


urlpatterns = [
    path('register/',Register_Users,name='register'),
    path('login/',login_user,name='login'),
    path('logout/',User_logout,name='logout'),
]