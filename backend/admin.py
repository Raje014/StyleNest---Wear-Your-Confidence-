from django.contrib import admin
from .models import *

"""
class category_returns(admin.ModelAdmin):
    list_display = ('name','image','description')
admin.site.register(category,category_returns)
"""

admin.site.register(MainCategory)
admin.site.register(category)
admin.site.register(product)