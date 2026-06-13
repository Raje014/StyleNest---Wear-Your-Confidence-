from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
from .models import *
from django.contrib import messages
from frontend.form import CustomUserForm
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def dashboard(request):
    products = product.objects.filter(trending=1)
    return render(request, 'pages/dashboard.html',{'products':products})

def about(request):
    return render(request, 'pages/about.html')

# login page
def loginpage(request):
    if request.method == 'POST':
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