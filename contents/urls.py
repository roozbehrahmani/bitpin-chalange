from django.urls import path
from . import views


urlpatterns = [
    # token
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token-refresh'),

    # register
    path('register/', views.Register.as_view(), name="registration"),

    # login
    path('login/', views.Login.as_view(), name="login"),


]
