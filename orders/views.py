from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache

# Models
from orders.models import *

# Create your views here.
def index(request):
    return HttpResponse("Project 3: TODO")

def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        confirm = request.POST['password_confirmation']

        if not username or not email or not password or not confirm or not first_name or not last_name or password != confirm:
            messages.success(request, "There was an error with your registration")
            
            return redirect('register')

        try:
            user = User(username=username, email=email, first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.save()
            
        except Exception as e:
            messages.error(request, "There is a problem with your register data, try again.")
            return redirect('/register')
        
        messages.success(request, "Succesfully Registered!")
        return redirect('/login')

    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # Replace 'home' with the URL name of your home page
        else:
            messages.error(request, "Invalid username or password")
            return redirect('/login')
        
    return render(request, 'login.html')

def log_out(request):
    logout(request)
    return redirect('/login')

# @never_cache # This is to prevent caching of the page so pressing back button would not show auth protected content
def menu(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            sizes = Size.objects.all()
            pizza_types = PizzaType.objects.all()
            toppings = Topping.objects.all()
            
            data = {
                'sizes': sizes,
                'pizza_types': pizza_types,
                'toppings': toppings
            }
            return render(request, 'menu.html', data)
    else:
        return redirect('/login')
    
    
def pizza_price(request):
    if request.method == 'POST':
        size_id = request.POST.get('pizza_size')
        pizza_type_id = request.POST.get('pizza_type')
        toppings_count = request.POST.get('toppings_count')
        
        # print(size_id, pizza_type_id, toppings_count)
        # print()
        try:
            product_type = ProductType.objects.get(name='Pizza')
        except ProductType.DoesNotExist:
            return JsonResponse({'price': '1'})

        try:
            toppings_count_obj = ToppingCount.objects.get(toppings_count=toppings_count)
        except ToppingCount.DoesNotExist:
            return JsonResponse({'price': '2'})

        try:
            # print(size_id, pizza_type_id, toppings_count_obj.id, product_type.id)
            # print()

            pizza_detail = PizzaDetail.objects.get(
                # product_id=product_type.id,
                pizza_type=pizza_type_id,
                pizza_size=size_id,
                toppings_count=toppings_count_obj.id
            )
            
            # this is to make the data serializable
            product_id = pizza_detail.product_id.id  # Extract the primary key
            price = pizza_detail.product_id.price
            
            response = {
                'price': price,
                'product_id': product_id,
                'detail_id': pizza_detail.id,
            }

            return JsonResponse(response)
            
        except PizzaDetail.DoesNotExist:
            return JsonResponse({'price': '3'})

    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
    
    
def add_pizza_cart(request):
    if request.method == 'POST':
        product_instance = Product.objects.get(pk=request.POST.get('product_id'))
        # product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        toppings = request.POST.getlist('toppings[]')

        try:
            new_cart = Cart(
                user_id=request.user,
                product_id=product_instance,
                quantity=quantity
            )
            
            new_cart.save()
            
            if toppings != None:                       
                for i in toppings:
                    topping_instance = Topping.objects.get(pk=i)
                    new_topping_cart = ToppingsCart(
                        cart_id=new_cart,
                        topping_id=topping_instance
                    )   
                    new_topping_cart.save()                   
                                
            return JsonResponse({'title': 'Perfect!', 'message': 'Item saved to cart succesfully', 'type': 'success'}) 
        except:
            return JsonResponse({'title': 'Oops!', 'message': 'Could not save item to cart', 'type': 'error'}) 

    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)