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
]