from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    pass


# class Author(models.Model):
#     name = models.CharField(max_length=50)
#     address = models.CharField(max_length=100)

# class Book(models.Model):
#     title = models.CharField(max_length=100)
#     author = models.ForeignKey(Author, on_delete=models.CASCADE)


# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField
#     price = models.DecimalField(max_digits=6, decimal_places=2)
#     stock = models.PositiveIntegerField()
#     image = models.ImageField(upload_to='products/')

#     @property
#     def in_stock(self):
#         return self.stock > 0
    
#     def __str__(self):
#         return f"{self.name}"


# class Order(models.Model):
#     class StatusChoices(models.TextChoices):
#         PENDING = 'Pending'
#         CONFIRMED = "Confirmed"
#         CANCELLED = 'Cancelled'

    
#     orderId = models.UUIDField(default=uuid.uuid4)
#     products = models.ManyToManyField(Product, related_name='products', through='OrderItem')
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     status = models.TextChoices(choices=StatusChoices.choices, default = StatusChoices.PENDING)

#     def __str__(self):
#         return f"{self.orderId} by {self.user}"
    

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()

#     @property
#     def item_subtotal(self):
#         return self.product.price * self.quantity
    
#     def __str__(self):
#         return f" {self.quantity} x {self.product.name} in order {self.order.order_id}"
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    @property
    def in_stock(self):
        return self.stock > 0
    
    def __str__(self):
        return self.name
    
class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "Pending"
        CONFIRMED = 'Confirmed'
        CANCELLED = 'Cancelled'

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through= 'OrderItem', related_name="orders")
    status = models.CharField(max_length=20, 
                              choices=StatusChoices.choices,
                              default = StatusChoices.PENDING
                              )
    
    def __str__(self):
        return f" Order {self.order_id} by {self.user.username}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete= models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_name')
    quantity = models.PositiveIntegerField()

    @property
    def item_subtotal(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f" {self.quantity} x {self.product.name} in order {self.order.order_id}"
    


  



    
