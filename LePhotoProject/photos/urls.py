from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name="home"),
    path('', views.loginUser, name="login"),
    path('contact/', views.contact, name="contact"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    path('gallery/', views.gallery, name='gallery'),
    path('photo/<str:pk>/', views.viewPhoto, name='photo'),
    path('add/', views.addPhoto, name='add'),
    path('delete/<str:pk>',views.deletePhoto, name="delete"),
    
]