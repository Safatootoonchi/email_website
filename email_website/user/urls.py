from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginView.as_view(), name='user_login'),
    path('register/', views.RegisterView.as_view(), name='user_register'),
    path('validation-form/', views.validation_form, name="validation-form"),
    path('logout/', views.logout_view, name="logout"),

]
