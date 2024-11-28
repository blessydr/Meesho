from django.db import models
from django.contrib.auth.models import User  
from multiselectfield import MultiSelectField



class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Mens Wear', 'Men\'s Wear'),
        ('Womens Wear', 'Women\'s Wear'),
        ('Kids Wear', 'Kids\' Wear'),
        ('Accessories', 'Accessories'),
        ('Footwear', 'Footwear'),
        ('Sportswear', 'Sportswear'),
        ('Home Decor', 'Home Decor'),
        ('Electronics', 'Electronics'),
    ]
    size_choices = [('S', 'Small'), ('M', 'Medium'), ('L', 'Large'),('XXL','XXL'),('XL','XL'),('XXXL','XXXL')]
    name = models.CharField(max_length=100)  
    description = models.TextField()  
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    image = models.ImageField(upload_to='products/') 
    sizes = MultiSelectField(choices=size_choices)  
    colors = models.CharField(max_length=50)  
    availability = models.BooleanField(default=True)  
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    date_added = models.DateTimeField(auto_now_add=True) 
    date_updated = models.DateTimeField(auto_now=True)  
    brand = models.CharField(max_length=50, blank=True, null=True)  
    likes_count = models.IntegerField(default=0)
    
    
    
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(default=1)  
    review = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'product')


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlists') 
    created_at = models.DateTimeField(auto_now_add=True) 

    class Meta:
        unique_together = ('user', 'product')  




       
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=5, choices=Product.size_choices, default='M') 
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Cart of {self.user.username} - Product: {self.product.name} - Quantity: {self.quantity} - Total: {self.total_price}"

    class Meta:
        unique_together = ('user', 'product', 'size')