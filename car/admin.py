from django.contrib import admin
from . models import Product ,Customer ,Booking , Payment




# Register your models here.
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Booking)
admin.site.register(Payment)
