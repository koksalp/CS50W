from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout 
from django.urls import reverse 
from django.http import HttpResponse, HttpResponseRedirect  
from django.db import IntegrityError  
from django.http import JsonResponse 
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import * 
from .helpers import proper_string
import json 

# Create your views here. 

def index(request):   
    
    # options for sorting restaurants 
    options = ["all", "open", "closed"] 

    # handle POST request 
    if request.method == "POST": 

        # get sorting option
        sort = request.POST["sort"] 

        # sort query set 
        if sort == "all":
            restaurants = Restaurant.objects.all().order_by("-is_open", "name") 
        elif sort == "open": 
            restaurants = Restaurant.objects.filter(is_open=True).order_by("name") 
        elif sort == "closed": 
            restaurants = Restaurant.objects.filter(is_open=False).order_by("name")  

        # render page that lists restaurants in correct order 
        return render(request, "bringmyfood/index.html", {
            "restaurants": restaurants,  
            "options": options,   
            "selected": sort   
        })  

    # handle GET request 
    # sort restaurants, open/close first then alphabetical  
    restaurants = Restaurant.objects.all().order_by("-is_open", "name") 

    # render homepage 
    return render(request, "bringmyfood/index.html", {
        "restaurants": restaurants,  
        "options": options,   
        "selected": options[0]   
    })  

def login_view(request): 

    # handle POST request 
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"] 

        # verify credentials 
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user) 

            # show homepage 
            return HttpResponseRedirect(reverse("index"))
        else: 

            # show login page with an error message 
            return render(request, "bringmyfood/login.html", {
                "message": "Invalid username and/or password."
            }) 

    # handle GET request 
    else: 

        # show homepage 
        return render(request, "bringmyfood/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request): 

    # handle POST request 
    if request.method == "POST": 

        # get user input 
        username = request.POST["username"]
        email = request.POST["email"]

        # username can not exceed 12 characters 
        if len(username) > 12: 
            return render(request, "bringmyfood/register.html", {
                "message": "Username is too long." 
            }) 
             
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"] 

        # passwords do not match 
        if password != confirmation:
            return render(request, "bringmyfood/register.html", {
                "message": "Passwords must match."
            })

        # password or confirmation fields can not be empty 
        if not password or not confirmation: 
            return render(request, "bringmyfood/register.html", {
                "message": "Password fields can not be empty." 
            }) 

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "bringmyfood/register.html", {
                "message": "Username already taken."
            })
            
        # check if register type is customer 
        try: 
            register_type = request.POST['register_customer'] 

        # register user as owner 
        except: 
            user.is_owner = True 
            user.save() 

            # each restaurant owner is also customer 
            Customer(person=user, balance=0).save() 
            Owner(person=user).save() 
            
            # log user in 
            login(request, user)

            # show homepage 
            return HttpResponseRedirect(reverse("index")) 

        # register user as customer 
        else: 
            Customer(person=user, balance=0).save()       
            login(request, user)

            return HttpResponseRedirect(reverse("index"))

    # handle GET request 
    else: 

        # show register page 
        return render(request, "bringmyfood/register.html") 

@login_required()  
def orders(request, user_id: int): 

    # check if such user exists  
    user = User.objects.filter(pk=user_id).first() 
    customer = Customer.objects.filter(person=user).first()  

    # if user does not exist, redirect to homepage 
    if not user:
        return HttpResponseRedirect(reverse("index")) 
    if not customer: 
        return HttpResponseRedirect(reverse("index")) 
 
    # render page that shows all customer orders  
    return render(request, "bringmyfood/orders.html", {
        "orders": Order.objects.filter(customer=customer).order_by("-created_at"),  
        "amounts": Amount.objects.all()      
    }) 

@login_required() 
def profile(request, user_id: int):

    # check if such user exists   
    user = User.objects.filter(pk=user_id).first() 
    customer = Customer.objects.filter(person=user).first()  
    
    # if not, show error message 
    if not user or not customer: 
            return render(request, "bringmyfood/profile.html", { 
                "message": "Invalid User", 
                "error": True 
            }) 

    # user attempts to add money to his/her customer account 
    if request.method=="POST": 
        try: 
            amount = float(request.POST["amount"]) 
        except ValueError: 
            return render(request, "bringmyfood/profile.html", { 
                "customer": customer, 
                "message": "Amount must be a number." 
            }) 
        else: 
            if amount < 0: 
                return render(request, "bringmyfood/profile.html", {
                    "customer": customer, 
                    "message": "Amount must be greater than 0." 
                }) 
            else: 
                customer.balance = customer.balance + amount
                customer.save()  
                return render(request, "bringmyfood/profile.html", { 
                    "customer": customer, 
                    "message": f"${amount} has been successfully added to your customer account."
                }) 
    
    # user reaches page via GET request, render profile page 
    return render(request, "bringmyfood/profile.html", { 
        "customer": customer 
    }) 

@login_required()
def owner_manage(request, user_id: int):  

    # get restaurant owner 
    owner = Owner.objects.get(person=User.objects.get(pk=user_id)) 
    restaurants = owner.owned.all() 
    
    # new restaurant attempts to opened  
    if request.method == "POST": 

        # get restaurant info 
        name = request.POST["restaurant_name"].upper() 
        address = request.POST["restaurant_address"].capitalize() 
        category = request.POST["category"].upper() 
        phone_number = request.POST["phone_number"] 

        # restaurant already owned 
        if owner.owned.filter(name=name): 
            return render(request, "bringmyfood/owner_manage.html", {
                "message": f"You already have a restaurant with the name {name}",    
                "restaurants": restaurants                
            })  

        # if any one of the fields is missing, show error message 
        if not all([name, address, category, phone_number]): 
            return render(request, "bringmyfood/owner_manage.html", {
                "message": "Name, address, category and phone number fields cannot be empty.",    
                "restaurants": restaurants               
            })  


        restaurant = Restaurant(
            name=name, 
            address=address, 
            category=category, 
            phone_number=phone_number,  
            owner=owner 
        ) 

        restaurant.save() 
        
        return render(request, "bringmyfood/owner_manage.html", {
            "created": True, 
            "restaurant_name": restaurant.name,      
            "restaurants": restaurants      
        })  
    return render(request, "bringmyfood/owner_manage.html", 
    {
        "restaurants": restaurants 
    })       

@csrf_exempt
@login_required 
def restaurant(request, restaurant_id: int): 

    # get restaurant 
    res = Restaurant.objects.filter(pk=restaurant_id).first() 

    # check if restaurant is valid 
    if not res: 
        return render(request, "bringmyfood/restaurant.html", {
            "message": "Invalid Restaurant" 
        }) 

    # a dict of items to pass to render function    
    context = { 
        "restaurant": res, 
        "amounts": Amount.objects.all(),      
        "balance": Customer.objects.get(pk=request.user.id).balance   
    } 

    # restaurant owner attempts to add new product to menu 
    if request.method == "POST": 

        # put user input into a certain format     
        product_name = proper_string(request.POST["product_name"]) 

        # show error message if the product already exists    
        if Product.objects.filter(name=product_name): 
            context["message"] = f"{product_name} already exists" 
            return render(request, "bringmyfood/restaurant.html", context) 

        # product name is empty 
        if not product_name: 
            context["message"] = "Product name is empty" 
            return render(request, "bringmyfood/restaurant.html", context) 

        # error checking  
        try:
            product_price = float(request.POST["product_price"]) 
        except ValueError: 
            context["message"] = "Price should be a number" 
            return render(request, "bringmyfood/restaurant.html", context) 
        else: 
            try:
                product_calories = int(request.POST["product_calories"]) 
            except ValueError: 
                context["message"] = "Calories should be integer" 
                return render(request, "bringmyfood/restaurant.html", context) 
            else: 
                if not product_calories: 
                    context["message"] = "Calories field cannot be empty" 
                    return render(request, "bringmyfood/restaurant.html", context) 

                product_image_url = request.POST["product_image_url"] 
                
                if not product_image_url: 
                    context["message"] = "Image field cannot be empty" 
                    return render(request, "bringmyfood/restaurant.html", context) 

                if len(product_image_url) > 255: 
                    context["message"] = "URL is too long"  
                    return render(request, "bringmyfood/restaurant.html", context) 
                
                Product(name=product_name, price=product_price, calories=product_calories, belong=res, image=product_image_url).save() 
                context["message"] = f"{product_name} has been successfully added to {res.name}" 
                
                return render(request, "bringmyfood/restaurant.html", context)   
            
    # handle PUT request 
    elif request.method == "PUT": 

        # get data 
        data = json.loads(request.body) 
        order_id = data["order_id"]  
        delete = data["delete"] 
        has_restaurant_deleted =data["has_restaurant_deleted"]  
        
        # get order 
        order = Order.objects.filter(pk=order_id).first()  
        
        # perform one of the operations 
        if order: 
            if delete: 
                print("deleted") 
                order.delete() 
            elif has_restaurant_deleted:  
                print("restaurant has deleted ") 
                order.has_restaurant_deleted = True  
                order.save()      
            else: 
                print("deactivated") 
                order.is_active = False 
                order.save()  

            # success 
            return JsonResponse({"message": "accepted"}, status=204) 

        # failure 
        return JsonResponse({"message": "rejected"}, status=404) 

    # page is accessed via GET request, render page 
    else: 
        return render(request, "bringmyfood/restaurant.html", { 
            "restaurant": res, 
            "amounts": Amount.objects.all(),      
            "balance": Customer.objects.get(pk=request.user.id).balance 
        })  

@login_required  
def product(request, product_id: int): 

    # get product 
    product = Product.objects.filter(pk=product_id).first()

    # product not found 
    if not product: 
        return render(request, "bringmyfood/product.html", {
            "message": "Invalid Product" 
        }) 

    # render product page   
    return render(request, "bringmyfood/product.html", {
        "product": product 
    })    
  
@csrf_exempt
@login_required 
def order(request): 

    # POST requests only 
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400) 

    # get data 
    data = json.loads(request.body) 

    # get objects 
    user = User.objects.get(pk=request.user.id) 
    customer = Customer.objects.get(person=user)
    first_product = Product.objects.get(pk=int(list(data.keys())[0])) 
    restaurant = Restaurant.objects.get(pk=first_product.belong.pk)  

    # create a new order 
    order = Order(customer=customer, restaurant=restaurant) 
    order.save() 
    
    # handle product amounts 
    for product_id in data: 
        quantity = data[product_id] 
        if quantity > 0: 
            product_id = int(product_id) 
            product = Product.objects.get(pk=product_id)
            
            order.products.add(product) 
            order.total = order.total + product.price * quantity 
            order.save() 
            Amount(product=product, order=order, amount=quantity).save() 
        elif quantity == 0:
            continue 

        # something is wrong, delete the order 
        else : 
            order.delete()
            return JsonResponse({"data": data, "status": False, "balance": customer.balance, "order_total": order.total, "error": True}) 
            
    # customer can not afford order 
    if customer.balance < order.total:   
        order.delete()        
        return JsonResponse({"data": data, "status": False, "balance": customer.balance, "order_total": order.total}) 
        
    # calculate customer balance after paying  
    customer.balance = round(customer.balance - order.total, 2) 
    customer.save()   
    
    return JsonResponse({"data": data, "status": True, "balance": customer.balance, "order_total": order.total})    