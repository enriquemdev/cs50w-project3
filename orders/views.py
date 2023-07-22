from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist

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
            sub_types = SubType.objects.all()
            
            extraType = ProductType.objects.get(pk=3)
            extras = Product.objects.filter(product_type_id=extraType)
            
            pastaType = ProductType.objects.get(pk=4)
            pastas = Product.objects.filter(product_type_id=pastaType)
            
            saladType = ProductType.objects.get(pk=5)
            salads = Product.objects.filter(product_type_id=saladType)
            
            dps = DinnerPlatterType.objects.all()
                
            print(extraType)
            data = {
                'sizes': sizes,
                'pizza_types': pizza_types,
                'toppings': toppings,
                'sub_types': sub_types,
                'extras': extras,
                'pastas': pastas,
                'salads': salads,
                'dps': dps,
            }
            return render(request, 'menu.html', data)
    else:
        return redirect('/login')
    
def cart(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            
            images = {
                1: 'https://www.simplyrecipes.com/thmb/I4razizFmeF8ua2jwuD0Pq4XpP8=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/__opt__aboutcom__coeus__resources__content_migration__simply_recipes__uploads__2019__09__easy-pepperoni-pizza-lead-4-82c60893fcad4ade906a8a9f59b8da9d.jpg',
                2: 'https://goodcheapeats.com/wp-content/uploads/2021/06/two-italian-subs-square-no-bg-green.jpg',
                4: 'https://images.immediate.co.uk/production/volatile/sites/30/2021/04/Pasta-alla-vodka-f1d2e1c.jpg',
                5: 'https://www.eatingwell.com/thmb/tOraypX2Z2ZztcmM2EhoppQW0jE=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc():focal(1219x879:1221x881)/chopped-power-salad-with-chicken-0ad93f1931524a679c0f8854d74e6e57.jpg',
                6: 'https://www.organizeyourselfskinny.com/wp-content/uploads/2022/02/chicken-meatball-parm-feature.jpg'
            }
                      
            user = request.user            
            
            cart_items = Cart.objects.filter(user_id=user, is_sold=False)

            # Retrieve the product information and sum the quantity, grouped by product_id
            aggregated_cart_items = cart_items.values('id', 'product_id', 'quantity', 'created_at').order_by('-created_at')

            # Create an empty list to store the final result
            result = []
            total_cart = 0

            # Iterate through each item in the aggregated_cart_items queryset
            for item in aggregated_cart_items:
                # print(item)
                # Get the product associated with this item
                product = Product.objects.get(id=item['product_id'])
                
                item['total_price'] = product.price * item['quantity']
                # Get all toppings related to this cart item
                toppings = ToppingsCart.objects.filter(cart_id=item['id']).select_related('topping_id')
                
                # Get all extras related to this cart item
                extras = ExtrasCart.objects.filter(cart_id=item['id']).select_related('extra_id')
                
                # Calculate the total price of extras for this cart item
                total_extras_price = sum(extra.extra_id.price for extra in extras)
                
                # Create a dictionary to store the required information for this cart item
                cart_data = {
                    'cart_id': item['id'],
                    'product': product,
                    'quantity': item['quantity'],
                    'toppings': list(toppings),
                    'extras': list(extras),
                    # 'total_extras_price': total_extras_price,
                    # 'total_price': item['total_price'],
                    'total_final_price': item['total_price'] + total_extras_price,
                    'date': item['created_at'],
                    'image': images[product.product_type_id.id],
                }
                
                total_cart += cart_data['total_final_price']
                
                # Append the cart_data to the result list
                result.append(cart_data)
                


            return render(request, 'cart.html', {'cart_items': result, 'total_cart': total_cart})
    else:
        return redirect('/login')
    
def orders(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            
            images = {
                1: 'https://www.simplyrecipes.com/thmb/I4razizFmeF8ua2jwuD0Pq4XpP8=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/__opt__aboutcom__coeus__resources__content_migration__simply_recipes__uploads__2019__09__easy-pepperoni-pizza-lead-4-82c60893fcad4ade906a8a9f59b8da9d.jpg',
                2: 'https://goodcheapeats.com/wp-content/uploads/2021/06/two-italian-subs-square-no-bg-green.jpg',
                4: 'https://images.immediate.co.uk/production/volatile/sites/30/2021/04/Pasta-alla-vodka-f1d2e1c.jpg',
                5: 'https://www.eatingwell.com/thmb/tOraypX2Z2ZztcmM2EhoppQW0jE=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc():focal(1219x879:1221x881)/chopped-power-salad-with-chicken-0ad93f1931524a679c0f8854d74e6e57.jpg',
                6: 'https://www.organizeyourselfskinny.com/wp-content/uploads/2022/02/chicken-meatball-parm-feature.jpg'
            }
                      
            user = request.user       
            
            # Get all the sales made of the currrent user
            sales = Sale.objects.filter(user_id=user)
            
            # Here we gonna save dicts with sale info and the cart items involved
            sales_info = []
            
            for sale in sales:
            
                # Carefully watch how we get the items related to each sale using the inverse relationship Cart items have with sale_details
                cart_items = Cart.objects.filter(sale_detail__sale_id=sale)

                # The rest is just the same as the cart template, only now we make it several times
                
                # Retrieve the product information and sum the quantity, grouped by product_id
                aggregated_cart_items = cart_items.values('id', 'product_id', 'quantity', 'created_at').order_by('-created_at')

                # Create an empty list to store the final result
                result = []
                total_cart = 0

                # Iterate through each item in the aggregated_cart_items queryset
                for item in aggregated_cart_items:
                    # print(item)
                    # Get the product associated with this item
                    product = Product.objects.get(id=item['product_id'])
                    
                    item['total_price'] = product.price * item['quantity']
                    # Get all toppings related to this cart item
                    toppings = ToppingsCart.objects.filter(cart_id=item['id']).select_related('topping_id')
                    
                    # Get all extras related to this cart item
                    extras = ExtrasCart.objects.filter(cart_id=item['id']).select_related('extra_id')
                    
                    # Calculate the total price of extras for this cart item
                    total_extras_price = sum(extra.extra_id.price for extra in extras)
                    
                    # Create a dictionary to store the required information for this cart item
                    cart_data = {
                        'cart_id': item['id'],
                        'product': product,
                        'quantity': item['quantity'],
                        'toppings': list(toppings),
                        'extras': list(extras),
                        'total_final_price': item['total_price'] + total_extras_price,
                        'date': item['created_at'],
                        'image': images[product.product_type_id.id],
                    }
                    
                    total_cart += cart_data['total_final_price']
                    
                    # Append the cart_data to the result list
                    result.append(cart_data)
                
                # at the end of the iteration of a sale, we save the sale info and the carts involved
                sale_data = {
                    'carts_data': result,
                    'sale_data': sale,
                }
                
                # And append it to the list
                sales_info.append(sale_data)  
                
            # print(sales_info)
                
            return render(request, 'orders.html', {'sales': sales_info})
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
    
    
def sub_price(request):
    if request.method == 'POST':
        size_id = request.POST.get('sub_size')
        sub_type_id = request.POST.get('sub_type')
        extras_ids = request.POST.getlist('extras[]')

        try:
            sub_detail = SubDetail.objects.get(
                sub_type=sub_type_id,
                sub_size=size_id,
            )
            
            # this is to make the data serializable
            product_id = sub_detail.product_id.id  # Extract the primary key
            price = sub_detail.product_id.price
            
            # Now its time to check for extras prices
            
            if extras_ids != None:
                for i in extras_ids:
                    extra_instance = Product.objects.get(pk=i)
                    print(extra_instance.price)
                    price += extra_instance.price
            
            response = {
                'price': price,
                'product_id': product_id,
                'detail_id': sub_detail.id,
            }

            return JsonResponse(response)
            
        except SubDetail.DoesNotExist:
            return JsonResponse({'price': 'error'})

    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
    
    
def add_sub_cart(request):
    if request.method == 'POST':
        product_instance = Product.objects.get(pk=request.POST.get('product_id'))
        quantity = request.POST.get('quantity')
        extras_ids = request.POST.getlist('extras[]')

        try:
            new_cart = Cart(
                user_id=request.user,
                product_id=product_instance,
                quantity=quantity
            )
            
            new_cart.save()
            
            if extras_ids != None:
                for i in extras_ids:
                    extra_instance = Product.objects.get(pk=i)
                    new_extras_cart = ExtrasCart(
                        cart_id=new_cart,
                        extra_id=extra_instance
                    )   
                    new_extras_cart.save() 
                    print('aja')
                                
            return JsonResponse({'title': 'Perfect!', 'message': 'Item saved to cart succesfully', 'type': 'success'}) 
        except:
            return JsonResponse({'title': 'Oops!', 'message': 'Could not save item to cart', 'type': 'error'}) 

    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
    
    
def add_pasta_cart(request):
    if request.method == 'POST':
        product_instance = Product.objects.get(pk=request.POST.get('product_id'))
        quantity = request.POST.get('quantity')

        try:
            new_cart = Cart(
                user_id=request.user,
                product_id=product_instance,
                quantity=quantity
            )
            
            new_cart.save()
                                
            return JsonResponse({'title': 'Perfect!', 'message': 'Item saved to cart succesfully', 'type': 'success'}) 
        except:
            return JsonResponse ({'title': 'Oops!', 'message': 'Could not save item to cart', 'type': 'error'}) 

    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
    

def add_salad_cart(request):
    if request.method == 'POST':
        product_instance = Product.objects.get(pk=request.POST.get('product_id'))
        quantity = request.POST.get('quantity')

        try:
            new_cart = Cart(
                user_id=request.user,
                product_id=product_instance,
                quantity=quantity
            )
            
            new_cart.save()
                                
            return JsonResponse({'title': 'Perfect!', 'message': 'Item saved to cart succesfully', 'type': 'success'}) 
        except:
            return JsonResponse ({'title': 'Oops!', 'message': 'Could not save item to cart', 'type': 'error'}) 

    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
    

def dp_price(request):
    if request.method == 'POST':
        size_id = request.POST.get('dp_size')
        dp_type_id = request.POST.get('dp_type')

        try:
            dp_detail = DinnerPlatterDetail.objects.get(
                dp_type=dp_type_id,
                dp_size=size_id,
            )
            
            # this is to make the data serializable
            product_id = dp_detail.product_id.id  # Extract the primary key
            price = dp_detail.product_id.price
            
            response = {
                'price': price,
                'product_id': product_id,
                'detail_id': dp_detail.id,
            }

            return JsonResponse(response)
            
        except DinnerPlatterDetail.DoesNotExist:
            return JsonResponse({'price': 'error'})

    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
    
    
def add_dp_cart(request):
    if request.method == 'POST':
        product_instance = Product.objects.get(pk=request.POST.get('product_id'))
        quantity = request.POST.get('quantity')
        extras_ids = request.POST.getlist('extras[]')

        try:
            new_cart = Cart(
                user_id=request.user,
                product_id=product_instance,
                quantity=quantity
            )
            
            new_cart.save()
            
            if extras_ids != None:
                for i in extras_ids:
                    extra_instance = Product.objects.get(pk=i)
                    new_extras_cart = ExtrasCart(
                        cart_id=new_cart,
                        extra_id=extra_instance
                    )   
                    new_extras_cart.save() 
                    print('aja')
                                
            return JsonResponse({'title': 'Perfect!', 'message': 'Item saved to cart succesfully', 'type': 'success'}) 
        except:
            return JsonResponse({'title': 'Oops!', 'message': 'Could not save item to cart', 'type': 'error'}) 

    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
  
        
def place_order(request):
    if request.method == 'POST':
        user = request.user
        try:
            cart_items = Cart.objects.filter(user_id=user, is_sold=False)
        except ObjectDoesNotExist:
            # Aquí manejas la excepción si no se encuentran elementos en el carrito
            error_message = "El carrito no contiene elementos."
            return JsonResponse({'error': error_message})
        except Exception as e:
            # Aquí manejas otras excepciones que puedan ocurrir durante la consulta
            error_message = f"Se produjo un error en la consulta: {e}"
            return JsonResponse({'error': error_message})

        try:
            new_sale = Sale(
                user_id=user,
                total=request.POST.get('total'),
            )
            
            new_sale.save()
            
            for cart in cart_items:
                cart.is_sold = True
                cart.save()
                
                new_sale_detail = Sale_Detail(
                    sale_id=new_sale,
                    cart_id=cart,
                )
                new_sale_detail.save()
            return JsonResponse({'message': "Order placed succesfully"})
        except Exception as e:
            # Aquí manejas otras excepciones que puedan ocurrir durante la consulta
            error_message = f"Se produjo un error en la consulta: {e}"
            return JsonResponse({'error': error_message})

    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)