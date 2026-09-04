from django.db import models
from django.contrib.auth.models import User
import datetime
import os 

# filename = pant.jpg => new_filename = 20260612123655pant.jpg => uploads/20260612123655pant.jpg
def getfilename(request,filename):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename = '%s%s'%(now_time,filename)
    return os.path.join('uploads/',new_filename)

# create a table category in database
class MainCategory(models.Model):
    name = models.CharField(max_length=200,null=False,blank=False)
    image = models.ImageField(upload_to=getfilename,null=True,blank=True)
    description = models.TextField(max_length=500,null=False,blank=False)
    status = models.BooleanField(default=False,help_text='0-show,1-hide')
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name

# create a table category in database
class category(models.Model):
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200,null=False,blank=False)
    image = models.ImageField(upload_to=getfilename,null=True,blank=True)
    description = models.TextField(max_length=500,null=False,blank=False)
    status = models.BooleanField(default=False,help_text='0-show,1-hide')
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name

# create a table product in database
class product(models.Model):
    category_name = models.ForeignKey(category,on_delete = models.CASCADE)
    name = models.CharField(max_length=200,null=False,blank=False)
    vendor_name = models.CharField(max_length=200,null=False,blank=False)
    product_image = models.ImageField(upload_to=getfilename,null=True,blank=True)
    description = models.TextField(max_length=500,null=False,blank=False)
    quantity = models.IntegerField(null=False,blank=False)
    original_price = models.FloatField(null=False,blank=False)
    selling_price = models.FloatField(null=False,blank=False)
    status = models.BooleanField(default=False,help_text='0-show,1-hide')
    trending = models.BooleanField(default=False,help_text = '0-default,1-trending')
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    Product = models.ForeignKey(product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add = True)

    # decorator
    @property
    def total_cost(self):
        return self.product_qty*self.Product.selling_price
    
class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Product = models.ForeignKey(product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

# cart history
class CartHistory(models.Model):
    ACTION_CHOICES = (
        ('ADDED', 'Added'),
        ('QUANTITY_INCREASED', 'Quantity Increased'),
        ('QUANTITY_DECREASED', 'Quantity Decreased'),
        ('REMOVED', 'Removed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Product = models.ForeignKey(product, on_delete=models.CASCADE)
    old_quantity = models.IntegerField(null=True, blank=True)
    new_quantity = models.IntegerField()
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.Product.name} - {self.action}"

# order and payment
class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PLACED','placed'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('RAZORPAY', 'Razorpay'),
        ('COD', 'Cash on Delivery'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    customer_name = models.CharField(max_length=150, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        null = True,
        blank= True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    Product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


class Payment(models.Model):
    STATUS_CHOICES = (
        ('CREATED', 'Created'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CREATED')
    failure_reason = models.TextField(null=True, blank=True)
    attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)