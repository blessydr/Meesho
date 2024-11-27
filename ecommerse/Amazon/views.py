from rest_framework import generics,filters
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login,logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Wishlist,Rating,Cart
from .serializers import ProductSerializer,ProductDetailSerializer,RatingSerializer,CartSerializer

class AddToCartView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self,request,product_id):
        user = request.user
        size = request.data.get('size', 'M')
        quantity = request.data.get('quantity', 1)
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        
        cart_item = Cart.objects.filter(user=user, product_id=product_id, size=size).first()
        
        if cart_item:

            cart_item.quantity += quantity
            cart_item.save()
            serializer = CartSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = CartSerializer(data={
                'user': user.id,
                'product': product.id,
                'size': size,
                'quantity': quantity,
            })
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
       
       
class CartListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)  
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        cart_items = self.get_queryset()
        
        total_cart_price = sum(item.product.price * item.quantity for item in cart_items)

        response.data = {
            "cart_items": response.data,
            "total_cart_price": total_cart_price
        }
        return response



class RemoveFromCart(APIView):
    def delete(self, request, *args, **kwargs):
        product_id = request.query_params.get('product_id')
        size = request.query_params.get('size')

        user = request.user

        cart_item = Cart.objects.filter(user=user, product_id=product_id, size=size).first()

        if cart_item:
            cart_item.delete()
            return Response({"message": "Item removed from cart."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Item not found in cart."}, status=status.HTTP_404_NOT_FOUND)




class RatingListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RatingSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Rating.objects.filter(product__id=product_id)

    def perform_create(self, serializer):
        product_id = self.kwargs['product_id']
        product = Product.objects.get(id=product_id)
        serializer.save(user=self.request.user, product=product)


class RatingDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RatingSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Rating.objects.filter(product__id=product_id, user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({"error": "You can only edit your own review."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'id' 
    
    
class WishlistView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]  
    serializer_class = ProductSerializer

    def get_queryset(self):
        user = self.request.user
        return Product.objects.filter(wishlists__user=user)

    def post(self, request):
        user = request.user
        product_id = request.data.get('product_id')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        wishlist_item, created = Wishlist.objects.get_or_create(user=user, product=product)

        if not created:
            wishlist_item.delete()
            product.likes_count = product.wishlists.count() 
            product.save()
            return Response({"message": "Removed from wishlist"}, status=status.HTTP_200_OK)
        
        product.likes_count = product.wishlists.count()
        product.save()
    
        return Response({"message": "Added to wishlist"}, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    def post(self, request):
        logout(request)  # This will end the user's session
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all() 
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['category', 'price', 'availability', 'name']
    search_fields = ['name', 'description', 'category']
    
    
    
class LoginView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user) 
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)



class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  
