from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),    
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),  
    path("my_orders/<int:user_id>", views.orders, name="orders"),        
    path("profile/<int:user_id>", views.profile, name="profile"),       
    path("owner_manage/<int:user_id>", views.owner_manage, name="owner_manage"), 
    path("restaurant/<int:restaurant_id>", views.restaurant, name="restaurant"), 
    path("product/<int:product_id>", views.product, name="product"), 

    # API route             
    path("order", views.order, name="order")    
]
