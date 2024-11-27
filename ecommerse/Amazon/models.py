from django.db import models
from django.contrib.auth.models import User  



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
    size_choices = [('S', 'Small'), ('M', 'Medium'), ('L', 'Large')]
    name = models.CharField(max_length=100)  
    description = models.TextField()  
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    image = models.ImageField(upload_to='products/') 
    sizes = models.CharField(max_length=1,choices=size_choices)  
    colors = models.CharField(max_length=50)  
    availability = models.BooleanField(default=True)  
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    date_added = models.DateTimeField(auto_now_add=True) 
    date_updated = models.DateTimeField(auto_now=True)  
    brand = models.CharField(max_length=50, blank=True, null=True)  
    review_count = models.IntegerField(default=0) 
    ratings_count = models.IntegerField(default=0)  

    def update_rating_info(self):
        reviews = self.reviews.all()  
        if reviews.exists():
            total_reviews = reviews.count() 
            total_rating = sum(review.rating for review in reviews) 
            self.rating = total_rating / total_reviews  
            self.ratings_count = total_reviews  
            self.review_count = total_reviews  
        else:
            self.rating = 0.0
            self.ratings_count = 0
            self.review_count = 0
        self.save()
    def __str__(self):
        return self.name  


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlists') 
    created_at = models.DateTimeField(auto_now_add=True) 

    class Meta:
        unique_together = ('user', 'product')  




class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(default=1)  # Rating between 1 and 5
    review = models.TextField(blank=True, null=True)  # Optional review
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'product')

       
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=1, choices=Product.size_choices, default='M') 
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Cart of {self.user.username} - Product: {self.product.name} - Quantity: {self.quantity} - Total: {self.total_price}"

    class Meta:
        unique_together = ('user', 'product', 'size')