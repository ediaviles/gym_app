"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path, include

from HealthWebsite import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.TestAction, name="root"),
    path('mainpage', views.MainPageAction, name='mainpage'),
    path('profile-page', views.ProfilePageAction, name='profile-page'),
    path('daily-diary', views.DailyDiaryAction, name='daily-diary'),
    path('google-maps', views.GoogleMapsAction, name='google-maps'),
    path('testing', views.TestAction, name='testing'),
    
    path('maps', views.MapsAction, name='maps'),
    path('gym-info', views.GymInfo, name='gym-info'),
    # path('user-address/<str:address>', views.UserAddress, name='user-address'),
    path('user-address', views.UserAddress, name='user-address'),
    path('gym-buddies', views.GymBuddies, name='gym-buddies'),
    path('accept-decline', views.AcceptDecline, name='accept-decline'),
    path('HealthWebsite/json-graph-data', views.UpdateGraph, name="json-graph-data"),
    # path('HealthWebsite/get-gyms/<int:lat>/<int:lng>/', views.GymLocations, name="get-gyms"),
    path('HealthWebsite/get-gyms/', views.GymLocations, name="get-gyms"),
    path('oauth/', include('social_django.urls', namespace='social')), 
    path('logout', auth_views.logout_then_login, name='logout'),
]
