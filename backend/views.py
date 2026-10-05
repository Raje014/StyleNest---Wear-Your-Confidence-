from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
from .models import *
from django.contrib import messages
from frontend.form import CustomUserForm
from django.contrib.auth import authenticate,login,logout
import json
from django.http import JsonResponse
from decimal import Decimal
from django.conf import settings
import razorpay
from rag.chatbot import answer_question

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

def update_cart_quantity(request, cid):
    if request.method == 'POST' and request.user.is_authenticated:

        data = json.loads(request.body)
        new_quantity = int(data.get('quantity'))

        try:
            cart_item = Cart.objects.get(
                id=cid,
                user=request.user
            )
        except Cart.DoesNotExist:
            return JsonResponse({
                'status': 'Cart item not found'
            }, status=404)

        if new_quantity < 1:
            return JsonResponse({
                'status': 'Quantity must be at least 1'
            }, status=400)

        if new_quantity > cart_item.Product.quantity:
            return JsonResponse({
                'status': 'Only limited stock available'
            }, status=400)

        old_quantity = cart_item.product_qty

        # Update cart
        cart_item.product_qty = new_quantity
        cart_item.save()

        # Save history
        if new_quantity > old_quantity:
            action = 'QUANTITY_INCREASED'
        elif new_quantity < old_quantity:
            action = 'QUANTITY_DECREASED'
        else:
            action = None

        if action:
            CartHistory.objects.create(
                user=request.user,
                Product=cart_item.Product,
                old_quantity=old_quantity,
                new_quantity=new_quantity,
                action=action
            )

        return JsonResponse({
            'status': 'Quantity updated'
        })

    return JsonResponse({
        'status': 'Invalid request'
    }, status=400)
    
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

# checkout page
def checkout(request):

    if not request.user.is_authenticated:
        return redirect('/login')

    # Check whether user came through Buy Now
    buy_now_product_id = request.session.get('buy_now_product_id')
    buy_now_quantity = request.session.get('buy_now_quantity')

    # -----------------------------
    # BUY NOW
    # -----------------------------
    if buy_now_product_id:

        try:
            buy_product = product.objects.get(
                id=buy_now_product_id,
                status=0
            )
        except product.DoesNotExist:
            messages.error(request, "Product not found.")
            return redirect('/')

        if not buy_now_quantity:
            buy_now_quantity = 1

        if buy_now_quantity > buy_product.quantity:
            messages.error(request, "Only limited stock available.")
            return redirect('/')

        checkout_items = [{
            'Product': buy_product,
            'product_qty': buy_now_quantity,
        }]

        is_buy_now = True

    # -----------------------------
    # NORMAL CART CHECKOUT
    # -----------------------------
    else:

        cart = Cart.objects.filter(user=request.user)

        if not cart.exists():
            messages.warning(request, "Your cart is empty.")
            return redirect('/cart')

        checkout_items = cart
        is_buy_now = False

    # -----------------------------
    # FORM SUBMISSION
    # -----------------------------
    if request.method == 'POST':

        customer_name = request.POST.get('customer_name')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        payment_method = request.POST.get('payment_method')

        # Calculate total
        total_amount = Decimal('0.00')

        for item in checkout_items:

            if is_buy_now:
                product_obj = item['Product']
                quantity = item['product_qty']
            else:
                product_obj = item.Product
                quantity = item.product_qty

            total_amount += (
                Decimal(str(product_obj.selling_price))
                * quantity
            )

        # Create Order
        order = Order.objects.create(
            user=request.user,
            customer_name=customer_name,
            mobile=mobile,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            payment_method=payment_method,
            total_amount=total_amount,
            status='PENDING'
        )

        # Create Order Items
        for item in checkout_items:

            if is_buy_now:
                product_obj = item['Product']
                quantity = item['product_qty']
            else:
                product_obj = item.Product
                quantity = item.product_qty

            unit_price = Decimal(str(product_obj.selling_price))
            total_price = unit_price * quantity

            OrderItem.objects.create(
                order=order,
                Product=product_obj,
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price
            )

        # Clear Buy Now session
        request.session.pop('buy_now_product_id', None)
        request.session.pop('buy_now_quantity', None)

        return redirect('order_review', order_id=order.id)

    # -----------------------------
    # SHOW CHECKOUT PAGE
    # -----------------------------
    return render(request, 'pages/checkout.html', {
        'cart': checkout_items,
        'user': request.user
    })

# order review page
def order_review(request, order_id):

    if not request.user.is_authenticated:
        return redirect('/login')

    try:
        order = Order.objects.get(
            id=order_id,
            user=request.user
        )
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('/cart')

    return render(request, 'pages/order_review.html', {
        'order': order,
        'items': order.items.all()
    })

# original place order
def place_order(request, order_id):

    if not request.user.is_authenticated:
        return redirect('/login')

    try:
        order = Order.objects.get(
            id=order_id,
            user=request.user
        )
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('/cart')

    if request.method != 'POST':
        return redirect('order_review', order_id=order.id)

    # COD
    if order.payment_method == 'COD':

        order.status = 'PLACED'
        order.save()

        for item in order.items.all():
            item.Product.quantity -= item.quantity
            item.Product.save()

        Cart.objects.filter(user=request.user).delete()

        return redirect('order_success', order_id=order.id)

    # Razorpay
    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    amount = int(order.total_amount * 100)

    razorpay_order = client.order.create({
        'amount': amount,
        'currency': 'INR',
        'receipt': f'order_{order.id}',
    })

    Payment.objects.create(
        order=order,
        razorpay_order_id=razorpay_order['id'],
        amount=order.total_amount,
        status='CREATED'
    )

    return render(request, 'pages/payment.html', {
        'order': order,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'amount': amount
    })

# order success page
def order_success(request, order_id):

    if not request.user.is_authenticated:
        return redirect('/login')

    order = Order.objects.get(
        id=order_id,
        user=request.user
    )

    return render(request, 'pages/order_success.html', {
        'order': order
    })

# buy now
def buy_now(request, pid):

    if not request.user.is_authenticated:
        return redirect('/login')

    try:
        Product = product.objects.get(
            id=pid,
            status=0
        )
    except product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect('/')

    # Get quantity selected on product page
    quantity = int(request.GET.get('quantity', 1))

    if quantity < 1:
        quantity = 1

    # Check stock
    if quantity > Product.quantity:
        messages.error(request, "Only limited stock available.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    # Store Buy Now product temporarily in session
    request.session['buy_now_product_id'] = Product.id
    request.session['buy_now_quantity'] = quantity

    return redirect('checkout')

# payment success
# Razorpay payment success
def payment_success(request):

    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'error',
            'message': 'Login required'
        })

    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid request'
        }, status=400)

    data = json.loads(request.body)

    razorpay_payment_id = data.get('razorpay_payment_id')
    razorpay_order_id = data.get('razorpay_order_id')
    razorpay_signature = data.get('razorpay_signature')

    try:
        payment = Payment.objects.get(
            razorpay_order_id=razorpay_order_id,
            order__user=request.user
        )
    except Payment.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Payment record not found'
        }, status=404)

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': payment.razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })

    except razorpay.errors.SignatureVerificationError:

        payment.status = 'FAILED'
        payment.failure_reason = 'Signature verification failed'
        payment.save()

        return JsonResponse({
            'status': 'error',
            'message': 'Payment verification failed'
        })

    # Payment verified successfully
    payment.razorpay_payment_id = razorpay_payment_id
    payment.razorpay_signature = razorpay_signature
    payment.status = 'SUCCESS'
    payment.save()

    order = payment.order
    order.status = 'PAID'
    order.save()

    # Reduce stock
    for item in order.items.all():
        item.Product.quantity -= item.quantity
        item.Product.save()

    # Clear cart
    Cart.objects.filter(user=request.user).delete()

    return JsonResponse({
        'status': 'success',
        'redirect_url': f'/order-success/{order.id}/'
    })


# chatbot
def chatbot_api(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST requests are allowed."},
            status=405
        )
    try:
        data = json.loads(request.body)
        question = data.get("message", "").strip()
        if not question:
            return JsonResponse(
                {"error": "Message cannot be empty."},
                status=400
            )
        answer = answer_question(question)
        return JsonResponse({
            "success": True,
            "response": answer
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)