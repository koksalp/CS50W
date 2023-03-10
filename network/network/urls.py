
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="follow"),
    path("profile/<int:user_id>", views.profile, name="profile"),                     

    
    # API routes
    path("posts/<int:post_id>", views.post, name="post"),
    path("handle_follow", views.handle_follow, name="handle_follow")
]
 
