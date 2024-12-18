from django.urls import path
from .views import RegisterUserView,LoginView,LogoutView,ProductListView,WishlistView,ProductDetailView,RatingDetailView,RatingListCreateView,CartListView,AddToCartView,RemoveFromCart
from. import views

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('ratings/', RatingListCreateView.as_view(), name='rating-list-create'),
    path('ratings/<int:product_id>/', RatingListCreateView.as_view(), name='rating-list-create-product'),
    path('ratingsedit/<int:pk>/', RatingDetailView.as_view(), name='rating-detail'),
    path('cart/list/', CartListView.as_view(), name='cart-list'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/remove/<int:pk>/', RemoveFromCart.as_view(), name='remove_from_cart'),


]
