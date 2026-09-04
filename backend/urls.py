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
    path('update_cart_quantity/<str:cid>',update_cart_quantity,name='update_cart_quantity'),
    path('checkout/', checkout, name='checkout'),
    path('order-review/<int:order_id>/', order_review, name='order_review'),
    path('place-order/<int:order_id>/', place_order, name='place_order'),
    path('order-success/<int:order_id>/', order_success, name='order_success'),
    path('buy-now/<int:pid>/', buy_now, name='buy_now'),
]