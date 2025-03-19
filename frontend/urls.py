from django.urls import path
from .views import signup_view, login_view, logout_view, home_view, delete_post_view

urlpatterns = [
    
    path("signup/", signup_view, name="signup"),
    path("", login_view, name="login"),
    path("home/", home_view, name="home"),
    path("logout/", logout_view, name="logout"),
    path("delete/<str:post_id>/", delete_post_view, name="delete_post"),

]
