from django.db import models
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


