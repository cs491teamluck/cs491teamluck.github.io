from django.urls import path

from . import views

urlpatterns = [
    path('deneme/', views.index, name='index'),
    path('signup/', views.SignupView.as_view()),
    path('login/',views.LoginView.as_view()),
    path('seeUser/',views.SeeUsersView.as_view()),

]