from django.urls import path


from .views import *
from .decorators.auth import unauthenticated_user

from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('register/', register, name='register'),
    path('login/', loginUser, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('cart/', Cart.as_view(), name='cart'),
    path('checkout/', CheckOut.as_view(), name='checkout'),
    path('orders/', unauthenticated_user(OrdersView.as_view()), name='orders'),

    # added
    path('search-product/', SearchProductView.as_view(), name='searchproduct'),
    path('productdetail/<int:id>/', ProductDetailView.as_view(), name="productdetail"),
    path('profile/<int:id>/', UserProfileView.as_view(), name='profile'),
    path('editprofile/<int:id>/', UserProfileEditView.as_view(), name='editprofile'),
    path('allproduct/', AllProductsView.as_view(), name="allproduct"),

    # cancel order
    path('cancel_order/', CancelCartView.as_view(), name="cancel"),

    # admin panel part
    path('admin-panel/', AdminPanelView.as_view(), name="adminpanel"),
    path('order-detail/<int:id>/', OrderDetailUpdateView.as_view(), name='orderdetail'),
    path('customer-full-detail/<int:id>/', CustomerFullDetailView.as_view(), name='customerfulldetail'),
    path('delete-order/<int:id>/', DeleteOrderView.as_view(), name="deleteorder"),
    path('admin-products/', AdminProductView.as_view(), name="adminproducts"),
    path('add-product/', AddProductView.as_view(), name="addproduct"),
    path('edit-product/<int:id>/', EditProductView.as_view(), name="editproduct"),
    path('delete-product/<int:id>/', DeleteProductView.as_view(), name="deleteproduct"),


]
