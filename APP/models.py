from django.db import models
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True


# Create your models here.



class Roles(models.Model):
    name=models.CharField(max_length=128)  
    description= models.CharField(max_length=200)
    
    # def __str__(self):
    #     return self.name
    
    class Meta:
     db_table = 'Main_Roles'

    
class User_roles(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    role= models.ForeignKey(Roles,on_delete=models.CASCADE)



class Seller(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)  
    business_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20,unique=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.business_name
    

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255, null=False)
    category = models.CharField(max_length=255, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    stock = models.CharField(max_length=20, default='Available', null=False)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True) 
    date_added = models.DateTimeField(auto_now_add=True)
    
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    full_name = models.CharField(max_length=255, null=False, blank=False)
    phone = models.CharField(max_length=15, null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    state = models.CharField(max_length=100, null=False, blank=False)
    zip_code = models.CharField(max_length=10, null=False, blank=False)
    country = models.CharField(max_length=100, null=False, blank=False)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} - {self.address}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_address = models.TextField(null=False, blank=False)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Prevents null
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Prevents null

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} in Order {self.order.id}"
