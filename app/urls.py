from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from . import views
from authentication.views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', include('categories.urls')),
    path('', include('weekdays.urls')),
    path('', include('genres.urls')),
    path('', include('kindrevenues.urls')),
    path('', include('graduations.urls')),
    path('', include('karatestyles.urls')),
    path('', include('dojos.urls')),
    path('', include('classes.urls')),
    path('', include('senseis.urls')),
    path('', include('expenses.urls')),
    path('', include('karatecas.urls')),
    path('', include('katas.urls')),
    path('', include('postures.urls')),
    path('', include('revenues.urls')),
    path('', include('inflows.urls')),
    path('', include('outflows.urls')),
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('', include('exams.urls')),
    path('', include('events.urls')),
    path('', include('dashboards.urls')),
    path('', include('examcategories.urls')),
    path('', include('invoices.urls')),
]

