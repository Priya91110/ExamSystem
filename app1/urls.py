from django.urls import path, include
from app1 import views

urlpatterns = [
    path('', views.index, name="home"),
    path('login/', views.login_view, name='login'),
    path('instructions/', views.instructions_view, name='instructions'),
    path('logout/', views.logout_view, name='logout'),
]
