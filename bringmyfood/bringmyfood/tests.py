from django.test import TestCase
from .models import * 
from random import randint, choice       
from random import randint     

# Create your tests here.

def createUser():
    for i in range(1, 11): 
        u = f"u{i}" 
        
        User(
            username = u, 
            first_name = "u", 
            last_name = str(i), 
            password = u, 
            email = f"{u}@gmail.com", 
            phone_number = str(i)    
        ).save() 

    return None 

def createCustomer():
    balance = 10 

    for user in User.objects.all(): 
        Customer(person = user, balance = balance).save()  
        balance += 10 

    return None 
 
def createRestaurant(): 
    restaurants = {
        "MCDONALD'S": "BURGER", 
        "STARBUCKS": "SNACK", 
        "SUBWAY": "SANDWICH", 
        "TACO BELL": "GLOBAL", 
        "CHICK-FIL-A": "CHICKEN",	 
        "WENDY'S": "BURGER", 
        "BURGER KING": "BURGER", 
        "DUNKIN'": "SNACK", 
        "DOMINO'S": "PIZZA", 
        "PANERA BREAD": "SANDWICH", 
        "FIVE GUYS": "SANDWICH",  
        "DAIRY QUEEN": "SANDWICH",  
        "ARBY'S": "SANDWICH",  
        "POPEYES": "SANDWICH",  
        "IN-N-OUT": "SANDWICH" 
    }  
    
    count = 1 

    for i in restaurants: 
        Restaurant(name=i, address=f"Address #{count}", category=restaurants[i], phone_number=count).save() 
        count += 1 
    return None 
    
if len(Restaurant.objects.all()) == 0: 
    print("restaurants created")
    createRestaurant() 

products = {
    "WAFFLE FRIES": {
        "price": 2.11 , 
        "restaurant": Restaurant.objects.filter(name="CHICK-FIL-A").first() 
    }, 
    "DOUBLE-DOUBLE": {
        "price": 4.04 , 
        "restaurant": Restaurant.objects.filter(name="IN-N-OUT").first() 
    }, 
    "FRIES": {
        "price": 2.29 , 
        "restaurant": Restaurant.objects.filter(name="MCDONALD'S").first() 
    }, 
    "CHICKEN": {
        "price": 6.77 , 
        "restaurant": Restaurant.objects.filter(name="POPEYES").first() 
    }, 
    "CHICKEN SANDWICH": {
        "price": 3.90 , 
        "restaurant": Restaurant.objects.filter(name="CHICK-FIL-A").first() 
    }, 
    "CURLY FRIES": {
        "price": 2.55 , 
        "restaurant": Restaurant.objects.filter(name="ARBY'S").first() 
    }, 
    "BLIZZARD": { 
        "price": 5.24 , 
        "restaurant": Restaurant.objects.filter(name="DAIRY QUEEN").first() 
    }, 
    "FROSTY": { 
        "price": 2.55 , 
        "restaurant": Restaurant.objects.filter(name="WENDY'S").first() 
    }, 
    "MCFLURRY": { 
        "price": 3.06 , 
        "restaurant": Restaurant.objects.filter(name="MCDONALD'S").first() 
    }, 
    "BACON CHEESEBURGER": { 
        "price": 11.12 , 
        "restaurant": Restaurant.objects.filter(name="FIVE GUYS").first() 
    }, 
} 

def createProduct():
    for product in products:
        Product(name=product, price=products[product]["price"], belong=products[product]["restaurant"]).save()     
        
def getProduct():
    random_p = choice(list(products.keys()))
    new = Product(name=random_p, price=products[random_p]["price"], belong=products[random_p]["restaurant"])
    new.save()  
    return new 

def createOrder(): 
    for r, c in zip(Restaurant.objects.all(), Customer.objects.all()):
        order = Order(customer = c, restaurant = r) 
        order.save() 
        for j in Product.objects.filter(belong=r):
            order.products.add(j) 
        
    return None  

def create():           
    createProduct() 
    createOrder()
    
users = User.objects.all() 
r = Restaurant.objects.all() 
c = Customer.objects.all() 
p = Product.objects.all() 
o = Order.objects.all() 

def delete():
    User.objects.all().delete()
    Restaurant.objects.all().delete() 
    Customer.objects.all().delete()
    Product.objects.all().delete()  
    Order.objects.all().delete()  

'''
r1=r[0]
r2=r[1]
r3=r[2]
r4=r[3]
r5=r[4]
''' 

def order(): 
    mcdonalds = Restaurant.objects.filter(name="MCDONALD'S").first()
    z = Owner.objects.get(person=User.objects.get(username="z"))
    if not mcdonalds in z.owned.all():
        z.owned.add(mcdonalds) 
    a=User.objects.get(username="a")
    ac = Customer.objects.get(person=a)
    order=Order(customer=ac, restaurant=mcdonalds)
    order.save() 
    products = mcdonalds.belong.all() 
    for i in products:
        order.products.add(i) 
        Amount(product=i, order=order, amount=randint(1, 10)).save()    

def true(orders=Restaurant.objects.filter(name="MCDONALD'S").first().prepared_by.all()):
    for i in orders:
        i.is_active = True 
        i.save()    

mcdonalds_list = [
    {
        "name": "BIG MAC", 
        "price": 3.99, 
        "calories": 530, 
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Big_Mac_hamburger.jpg/330px-Big_Mac_hamburger.jpg" 
    }, 
    {
        "name": "CHEESEBURGER", 
        "price": 1, 
        "calories": 290, 
        "image": "https://s7d1.scene7.com/is/image/mcdonalds/DC_202006_0003_Cheeseburger_StraightBun_832x472:product-header-desktop?wid=830&hei=458&dpr=off" 
    }, 
    {
        "name": "FILET-O-FISH", 
        "price": 3.79, 
        "calories": 390, 
        "image": "https://s7d1.scene7.com/is/image/mcdonalds/DC_202001_5926_Filet-O-Fish_HalfSlice_832x472:product-header-desktop?wid=830&hei=458&dpr=off" 
    }, 
    {
        "name": "QUARTER POUNDER WITH CHEESE", 
        "price": 3.79, 
        "calories": 520, 
        "image": "https://s7d1.scene7.com/is/image/mcdonalds/DC_202201_0007-005_QuarterPounderwithCheese_832x472:product-header-desktop?wid=830&hei=458&dpr=off" 
    }, 
    {
        "name": "SMOKY BLT DOUBLE QUARTER POUNDER WITH CHEESE", 
        "price": 7.49, 
        "calories": 990, 
        "image": "https://s7d1.scene7.com/is/image/mcdonalds/DC_202109_14866_SmokyBLTDoubleQuarterPounderwithCheese_832x472:product-header-desktop?wid=830&hei=456&dpr=off" 
    }, 
    {
        "name": "DOUBLE QUARTER POUNDER WITH CHEESE", 
        "price": 4.79, 
        "calories": 750, 
        "image": "https://s7d1.scene7.com/is/image/mcdonalds/202201_3426-005_DoubleQuarterPounderwithCheese_832x472:product-header-desktop?wid=830&hei=456&dpr=off" 
    }, 
    {
        "name": "SPICY DELUXE CRISPY CHICKEN SANDWICH", 
        "price": 4.99, 
        "calories": 530, 
        "image": "https://s7d1.scene7.com/is/image/mcdonalds/DC_202104_0100_DeluxeSpicyCrispyChickenSandwich_PotatoBun_832x472:product-header-desktop?wid=830&hei=458&dpr=off" 
    }, 
    {
        "name": "WORLD FAMOUS FRIES® (SMALL)", 
        "price": 1.39, 
        "calories": 230, 
        "image": "https://s7d1.scene7.com/is/image/mcdonalds/DC_202002_6050_SmallFrenchFries_Standing_832x472:product-header-desktop?wid=830&hei=456&dpr=off" 
    }, 
    {
        "name": "WORLD FAMOUS FRIES® (MEDIUM)", 
        "price": 1.79, 
        "calories": 320, 
        "image": "https://s7d1.scene7.com/is/image/mcdonalds/DC_202002_8932_MediumFries_832x472:product-header-desktop?wid=830&hei=458&dpr=off" 
    }, 
    {
        "name": "WORLD FAMOUS FRIES® (LARGE)", 
        "price": 1.89, 
        "calories": 480, 
        "image": "https://s7d1.scene7.com/is/image/mcdonalds/DC_202002_6053_LargeFries_832x472:product-header-desktop?wid=830&hei=456&dpr=off" 
    }, 
    {
        "name": "OREO® FUDGE MCFLURRY®", 
        "price": 4.39, 
        "calories": 460, 
        "image": "https://s7d1.scene7.com/is/image/mcdonalds/DC_202107_14883_OreoFudgeMcFlurry_832x472:product-header-desktop?wid=830&hei=458&dpr=off" 
    }, 
] 

chick_fil_a_list = [ 
    {
        "name": "CHICK-FIL-A CHICKEN SANDWICH", 
        "price": 3.05, 
        "calories": 440, 
        "image": "https://www.cfacdn.com/img/order/menu/Online/Entrees/Jul19_CFASandwich_pdp.png" 
    }, 
    {
        "name": "SPICY CHICKEN SANDWICH", 
        "price": 3.29, 
        "calories": 540, 
        "image": "https://www.cfacdn.com/img/order/menu/Online/Entrees/CFASpicySandwich_1080.png" 
    }, 
    {
        "name": "GRILLED CHICKEN CLUB SANDWICH", 
        "price": 5.59, 
        "calories": 520, 
        "image": "https://www.cfacdn.com/img/order/menu/Online/Entrees/grilledClub_colbyJack_PDP.png" 
    }, 
    {
        "name": "GRILLED CHICKEN COOL WRAP", 
        "price": 5.19, 
        "calories": 660, 
        "image": "https://www.cfacdn.com/img/order/menu/Online/Entrees/wrap_pdp.png" 
    }, 
    {
        "name": "SPICY CHICKEN DELUXE SANDWICH", 
        "price": 3.89, 
        "calories": 550, 
        "image": "https://www.cfacdn.com/img/order/COM/Menu_Refresh/Entree/Entree%20Desktop/_0003s_0012_%5BFeed%5D_0001s_0023_Entrees_Spicy-Deluxe-Sandwich.png" 
    }, 
    {
        "name": "CHICK-FIL-A NUGGETS (8 PC.)", 
        "price": 3.05, 
        "calories": 250, 
        "image": "https://www.cfacdn.com/img/order/menu/Online/Entrees/nuggets_8ct_PDP.png" 
    }, 
    {
        "name": "CHICK-FIL-A NUGGETS (12 PC.)", 
        "price": 4.45, 
        "calories": 380, 
        "image": "https://www.cfacdn.com/img/order/menu/Online/Entrees/nuggets_12ct_pdp_v2.png" 
    }, 
    {
        "name": "CHICK-FIL-A NUGGETS (30 PC.)", 
        "price": 14.69, 
        "calories": 950, 
        "image": "https://www.cfacdn.com/img/order/menu/Online/Entrees/30Nug_PDP.png" 
    }, 
    {
        "name": "CHICK-N-STRIPS (3 PC.)", 
        "price": 3.35, 
        "calories": 310, 
        "image": "https://www.cfacdn.com/img/order/menu/Online/Entrees/strips_3ct_PDP.png" 
    }, 
    {
        "name": "CHICK-N-STRIPS (4 PC.)", 
        "price": 4.39, 
        "calories": 410, 
        "image": "https://www.cfacdn.com/img/order/menu/Online/Entrees/strips_4ct_PDP.png" 
    }, 
] 

def create_product(): 
    mcdonalds = Restaurant.objects.filter(name="MCDONALD'S").first() 
    chick_fil_a = r.filter(name="CHICK-FIL-A").first()

    if mcdonalds: 
        for i in mcdonalds_list:
            add = True 
            for j in mcdonalds.belong.all(): 
                if j.name == i["name"]:  
                    add = False 
                    break 
            if add: 
                Product(name=i["name"], price=i["price"], calories=i["calories"], belong=mcdonalds, image=i["image"]).save()  

    if chick_fil_a: 
        for i in chick_fil_a_list: 
            add = True 
            for j in chick_fil_a.belong.all(): 
                if j.name == i["name"]: 
                    add = False 
                    break 
            if add: 
                Product(name=i["name"], price=i["price"], calories=i["calories"], belong=chick_fil_a, image=i["image"]).save()  
