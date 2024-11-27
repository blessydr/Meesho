from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product, Wishlist,Rating,Cart
from django.db.models import Sum, Count


class ProductDetailSerializer(serializers.ModelSerializer):
    offer_price = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    ratings_count = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = '__all__'
        
        
    def get_offer_price(self, obj):
        discount_amount = (obj.price * obj.discount) / 100
        offer_price = obj.price - discount_amount
        return round(offer_price, 2) 
  
    def get_review_count(self, obj):
        return Rating.objects.filter(product=obj).exclude(review__exact='').count()

    def get_ratings_count(self, obj):
        return Rating.objects.filter(product=obj).count()

  
class ProductSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)  # Read-only to ensure it's not modified through the API
    offer_price = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'offer_price', 'discount','likes_count','average_rating']
        
        
    def get_offer_price(self, obj):
        discount_amount = (obj.price * obj.discount) / 100
        offer_price = obj.price - discount_amount
        return round(offer_price, 2) 
    def get_average_rating(self, obj):
        aggregation = obj.ratings.aggregate(
            total_rating=Sum('rating'),
            rating_count=Count('rating')
        )
        print(total_rating)
        print(rating_count)
        total_rating = aggregation['total_rating'] or 0
        rating_count = aggregation['rating_count'] or 0
        if rating_count > 0:
            average = total_rating / rating_count
            return float(format(average, ".1f"))

        return 0  
