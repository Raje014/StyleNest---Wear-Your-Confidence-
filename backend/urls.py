from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('about/', about, name='about'),
    path('register/', register, name='register'),
    path('login/', loginpage, name='login'),
    path('logout/', logoutpage, name='logout'),
    path('collections/', collections, name='collections'),
    path('collections/<str:name>/', collectionDetail, name='collections'),
    path('collections/<str:cname>/<str:pname>', product_details, name='product_details'),
    path('addtocart', add_to_cart, name='addtocart'),
    path('cart', cart_page, name='cart'),
    path('deleted_product/<str:cid>', deleted_product, name='deleted_product'),
    path('favourite', favourite_page, name='favourite'),
    path('fav_view_page', fav_view_page, name='fav_view_page'),
    path('remove_fav/<str:fid>', remove_fav, name='remove_fav'),
]