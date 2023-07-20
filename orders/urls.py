from django.urls import path
# from django.contrib.auth.decorators import login_required


from . import views

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.user_login, name="user_login"),
    path("log_out", views.log_out, name="log_out"),
    path("not_login", views.index, name="index"),
    
    path("", views.menu, name="menu"),
    path("cart", views.cart, name="cart"),
    
    path("pizza_price", views.pizza_price, name="pizza_price"),
    path("add_pizza_cart", views.add_pizza_cart, name="add_pizza_cart"),
    path("sub_price", views.sub_price, name="sub_price"),
    path("add_sub_cart", views.add_sub_cart, name="add_sub_cart"),
    
    path("add_pasta_cart", views.add_pasta_cart, name="add_pasta_cart"),
    path("add_salad_cart", views.add_salad_cart, name="add_salad_cart"),
    
    path("dp_price", views.dp_price, name="dp_price"),
    path("add_dp_cart", views.add_dp_cart, name="add_dp_cart"),

]
