from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register([
    Size,
    PizzaType,
    ToppingCount,
    Topping,
    SubType,
    DinnerPlatterType,
    ProductType,
    Product,
    PizzaDetail,
    SubDetail,
    DinnerPlatterDetail,
    Cart,
    ToppingsCart,
    ExtrasCart,
    Sale,
    Sale_Detail
    ])