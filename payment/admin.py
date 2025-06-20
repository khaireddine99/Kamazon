from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.
@admin.register(Order)

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'created_at',
        'paid',
        'delivered',
    ]

    list_filter = [
       'paid',
       'delivered', 
    ]

admin.site.register(OrderItem)
