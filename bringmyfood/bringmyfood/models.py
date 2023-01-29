from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=16, blank=True)  
    is_owner = models.BooleanField(default=False) 
    
    def serialize(self):
        return {
            "user_id": self.pk, 
            "username": self.username,  
            "email": self.email, 
            "is_owner": self.is_owner,      
            "phone_number": self.phone_number,    
            "date_joined": self.date_joined, 
        } 

class Customer(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer") 
    balance = models.FloatField(default=0) 

    def __str__(self):
        return f"Customer name: {self.person.username} balance: {self.balance}" 

    def serialize(self):
        return {
            "user": self.person.serialize(), 
            "customer": {
                "customer_id": self.pk, 
                "balance": self.balance  
            }  
        }

class Owner(models.Model): 
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner") 

    def __str__(self):
        return f"Owner name: {self.person.username}"   
        
    def serialize(self):
        return {
            "user": self.person.serialize(), 
            "owner_id": self.pk 
        } 

class Restaurant(models.Model):
    name = models.CharField(max_length=64) 
    address = models.CharField(max_length=64) 
    category = models.CharField(max_length=16) 
    phone_number = models.CharField(max_length=16, blank=True) 
    is_open = models.BooleanField(default=True) 
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name="owned", blank=True, null=True)      

    def __str__(self):
        return f"Restaurant name: {self.name} category: {self.category}" 

    def serialize(self): 
        return {
            "name": self.name, 
            "id": self.pk, 
            "address": self.address, 
            "category": self.category, 
            "phone_number": self.phone_number, 
            "is_open": self.is_open,
            "owner": {
                "owner_id": self.owner.pk, 
                "user_related": self.owner.person.serialize()  
            }
        }

class Product(models.Model):
    name = models.CharField(max_length=64) 
    price = models.FloatField() 
    calories = models.IntegerField(default=0)  
    belong = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="belong", blank=True, null=True)   
    image = models.CharField(max_length=255, blank=True) 
 
    def __str__(self):
        return f"Product name: {self.name} price: {self.price} belongs to {self.belong.name if self.belong else 'no restaurant'}" 

    def serialize(self): 
        return {
            "name": self.name, 
            "price": self.price, 
            "belongs_to": self.belong.serialize() 
        } 

class Order(models.Model): 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="order_by", default="") 
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="prepared_by", default="") 
    created_at = models.DateTimeField(auto_now_add=True)  
    products = models.ManyToManyField(Product, blank=True, related_name="orders") 
    is_active = models.BooleanField(default=True) 
    has_restaurant_deleted = models.BooleanField(default=False)          
    total = models.FloatField(default=0) 

    def __str__(self):
        return f"customer: {self.customer.person.username} restaurant: {self.restaurant.name}"  
    
    def serialize(self): 
        return {
            "customer": self.customer.serialize(), 
            "restaurant": self.restaurant.serialize(), 
            "created_at": self.created_at, 
            "order_id": self.pk , 
            "products": [product.serialize() for product in self.products.all()] 
        } 
    
class Amount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="amount", blank=True, null=True)   
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order", blank=True, null=True)   
    amount = models.IntegerField(default=1, blank=True)

    def __str__(self):
        return f"Product name: {self.product.name} Product id: {self.product.pk} Order id: {self.order.pk} amount: {self.amount}" 

    def serialize(self):
        return {
            "product": self.product.serialize(), 
            "order": self.order.serialize(),
            "amount": self.amount        
        }  