from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from picApp import views
urlpatterns = [
    path('', views.Home.as_view(),name='home'),
    path('login/', views.login,name='login'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)