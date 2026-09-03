from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
from .models import *
from django.contrib import messages
from frontend.form import CustomUserForm
from django.contrib.auth import authenticate,login,logout
import json
from django.http import JsonResponse

# Create your views here.
def dashboard(request):
    products = product.objects.filter(trending=1)
    return render(request, 'pages/dashboard.html',{'products':products})

def about(request):
    return render(request, 'pages/about.html')

# login page
def loginpage(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        # check whether the method is post or not 
        if request.method == 'POST':
            # request.post => dictionary ah data ah store pannitu dic.get("username") => username ah get pannum
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in Successfully")
                return redirect('/')
            else:
                messages.error(request,"Invalid Username or Password")
                return redirect("/login")
        return render(request, 'pages/login.html')

def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Scuccessfully")
    return redirect("/")

def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Created Successfully.. Login Now...!")
            return redirect('/login')
    return render(request, 'pages/register.html',{'form': form})

def collections(request):
    # models ah idhula pass panna data ah idhula receive panni, template ah pass panrathu
    CategoryName = category.objects.filter(status=0)
    return render(request, "pages/collections.html", {'CategoryName': CategoryName})

def collectionDetail(request,name):
    # models ah idhula pass panna data ah idhula receive panni, template ah pass panrathu
    if(category.objects.filter(name=name,status=0)):
        products = product.objects.filter(category_name__name = name)
        return render(request, "products/product.html", {'products': products,'category_name': name}) #veriablename : view_name
    else:
        messages.warning(request, "No such Product Found")
        return redirect("collections")

def product_details(request,cname,pname):
    if(category.objects.filter(name=cname,status=0)):
        if(product.objects.filter(name=pname,status=0)):
            products = product.objects.filter(name=pname,status=0).first()
            return render(request, "products/product_details.html", {'products': products})

        else:
            messages.error(request,"No Such Category Found")
            return redirect('collections')
    else: 
        messages.error(request,"No Such Category Found")
        return redirect('collections')
    
# cart 
def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            product_qty = int(data['product_qty'])
            product_id = data['pid']
            product_status = product.objects.get(id=product_id)

            if product_status:
                if Cart.objects.filter(user = request.user.id, Product_id = product_id):
                    return JsonResponse({'status':'Product Already in cart'}, status=200)
                else:
                    if product_status.quantity >= product_qty:
                        Cart.objects.create(user = request.user, Product_id = product_id, product_qty = product_qty)
                        return JsonResponse({'status':'Product added to cart'}, status=200)
                    else:
                        return JsonResponse({'status':'Product out of stock'}, status=200)
        else:
            return JsonResponse({'status':'Login to Add product to cart'}, status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)

# cart page
def cart_page(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, "pages/cart.html", {"cart":cart})
    else:
        return redirect('/')
    
# deleted cart products
def deleted_product(request, cid):
    cart_item = Cart.objects.get(id=cid)
    cart_item.delete()
    return redirect("/cart")

# favourite products
def favourite_page(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            product_id = data['pid']
            product_status = product.objects.get(id=product_id)
            if product_status:
                if Favourite.objects.filter(user = request.user, Product_id = product_id):
                    return JsonResponse({'status':'Product already in Favourite'}, status=200)
                else:
                    Favourite.objects.create(user = request.user, Product_id = product_id)
                    return JsonResponse({'status':'Product added to Favourite'}, status=200)
        else:
            return JsonResponse({'status':'Login to Add product to Favourite'}, status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)

# favourite pagess
def fav_view_page(request):
    if request.user.is_authenticated:
        fav = Favourite.objects.filter(user=request.user)
        return render(request, "pages/favourite.html", {"fav":fav})
    else:
        return redirect('/')
    
# remove favourites
def remove_fav(request, fid):
    fav_item = Favourite.objects.get(id=fid)
    fav_item.delete()
    return redirect("/fav_view_page")