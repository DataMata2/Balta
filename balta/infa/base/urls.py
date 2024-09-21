from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('', views.home, name='home'),
    path('logout/', views.logoutPage, name='logout'),
    path('a-side/<int:q>', views.admin, name='a-side'),
    path('a-side/', views.admin, name='a-side'),
    path('create/', views.create, name='create'),
    path('delete/<int:pk>', views.delete, name='delete'),
    path('update/<int:pk>', views.update, name='update'),
]