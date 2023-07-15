from django.db import models
from django.utils import timezone
from django.conf import settings


# Create your models here.

# note: size can be one table as there are only 2 sizes for all products

# products_types
#  pizza, subs,  pasta, salad, dinner platters

# products: type + name + price(price if it is simple product(pasta and salad))

#pizza details: type + size + toppings count + price
# pizza types
# pizza sizes
# toppings count

# subs details: size + price
# subs sizes
# (keep in mind there is a sub that only have a large size)

# // Extras are only for subs
# They are gonna be treated like topping names, they are required on the order but not on the product
# so there will be a detail table for subs and pizzas selecting toppings and extras on the cart

# Pasta and Salad are simple

# Dinner platters details: size + price
# Dinner Platter sizes

class Size(models.Model):
    name = models.CharField(max_length=200, blank=False)
    
    def __str__(self):
        return self.name
# Small and Large

# Pizza catalogs
class PizzaType(models.Model):
    name = models.CharField(max_length=200, blank=False)
    def __str__(self):
        return self.name
# Regular and Sicilian

class ToppingCount(models.Model):
    name = models.CharField(max_length=200, blank=False)
    toppings_count = models.IntegerField()
    def __str__(self):
        return self.name + '__' + str(self.toppings_count)
# cheese = 0, 1, 2, 3, Special = 4

class Topping(models.Model):
    name = models.CharField(max_length=200, blank=False)
    def __str__(self):
        return self.name

# Sub Catalogs
class SubType(models.Model):
    name = models.CharField(max_length=200, blank=False)
    def __str__(self):
        return self.name
    
# Dinner Platter Catalogs
class DinnerPlatterType(models.Model):
    name = models.CharField(max_length=200, blank=False)
    def __str__(self):
        return self.name
    

class ProductType(models.Model):
    name = models.CharField(max_length=200, blank=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    product_type_id = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    def __str__(self):
        return self.name
    
class PizzaDetail(models.Model):
    # name = models.CharField(max_length=200, blank=False)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    pizza_type = models.ForeignKey(PizzaType, on_delete=models.CASCADE)
    pizza_size = models.ForeignKey(Size, on_delete=models.CASCADE)
    toppings_count = models.ForeignKey(ToppingCount, on_delete=models.CASCADE)
    # price = models.DecimalField(max_digits=8, decimal_places=2)
    def __str__(self):
        return f"{self.product_id.name} - {self.pizza_type.name} ({self.pizza_size.name}) with {self.toppings_count.toppings_count} toppings"
    
class SubDetail(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    sub_type = models.ForeignKey(SubType, on_delete=models.CASCADE)
    sub_size = models.ForeignKey(Size, on_delete=models.CASCADE)
    # price = models.DecimalField(max_digits=8, decimal_places=2)
    def __str__(self):
        return f"{self.product_id.name} - {self.sub_type.name} ({self.sub_size.name})"

    
# class Extra(models.Model):
#     product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200, blank=False)
#     price = models.DecimalField(max_digits=8, decimal_places=2)
    
class DinnerPlatterDetail(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    dp_type = models.ForeignKey(DinnerPlatterType, on_delete=models.CASCADE)
    dp_size = models.ForeignKey(Size, on_delete=models.CASCADE)
    # price = models.DecimalField(max_digits=8, decimal_places=2)
    def __str__(self):
        return f"{self.product_id.name} - {self.dp_type.name} ({self.dp_size.name})"
 
# Cart tables

class Cart(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE) # All product except extra
    quantity = models.IntegerField()
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        sold_status = "Sold" if self.is_sold else "Not Sold"
        return f"Cart #{self.pk} - User: {self.user_id.username}, Product: {self.product_id}, {sold_status}"
    
    # For when there is a product on cart that is pizza and has toppings
class ToppingsCart(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    topping_id = models.ForeignKey(Topping, on_delete=models.CASCADE)
    
    def __str__(self):
        cart_sold_status = "Sold" if self.cart_id.is_sold else "Not Sold"
        return f"ToppingsCart #{self.pk} - Cart #{self.cart_id.pk} ({cart_sold_status}), Topping: {self.topping_id.name}"
    
    # For when there is a product on cart that is sub and has extras
class ExtrasCart(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    extra_id = models.ForeignKey(Product, on_delete=models.CASCADE) # extra is a product
    
    def __str__(self):
        cart_sold_status = "Sold" if self.cart_id.is_sold else "Not Sold"
        return f"ExtrasCart #{self.pk} - Cart #{self.cart_id.pk} ({cart_sold_status}), Extra: {self.extra_id.name}"
    
class Sale(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    is_ready = models.BooleanField(default=False) # False is on preparation and True is ready
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Sale #{self.pk} - User: {self.user_id.username}, Total: {self.total}"

class Sale_Detail(models.Model):
    sale_id = models.ForeignKey(Sale, on_delete=models.CASCADE)
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE) # This turns the cart row into is_sold = true
    
    def __str__(self):
        username = self.cart_id.user_id.username
        product_name = self.cart_id.product_id.name
        return f"Sale Detail: Sale #{self.sale_id.pk} - User: {username}, Product: {product_name}"