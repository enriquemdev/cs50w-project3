from django.urls import path
# from django.contrib.auth.decorators import login_required


from . import views

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.user_login, name="user_login"),
    path("log_out", views.log_out, name="log_out"),
    path("not_login", views.index, name="index"),
    
    path("", views.menu, name="menu"),
    
    path("pizza_price", views.pizza_price, name="pizza_price"),
    path("add_pizza_cart", views.add_pizza_cart, name="add_pizza_cart"),
    path("sub_price", views.sub_price, name="sub_price"),
    path("add_sub_cart", views.add_sub_cart, name="add_sub_cart"),

]
