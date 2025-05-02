from django.urls import path, include
from app1 import views

urlpatterns = [
    path('', views.index, name="home"),
    path('login/', views.login_view, name='login'),
    path('instructions/', views.instructions_view, name='instructions'),
    path('logout/', views.logout_view, name='logout'),
    path('start-exam/', views.start_exam_view, name='start_exam'),
    path('submit-exam/', views.submit_exam_view, name='submit_exam'),
    path('thank-you/', views.thank_you_view, name='thank_you'),
]
