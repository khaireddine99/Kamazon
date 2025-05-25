from django.contrib import admin
from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'category',
        'sub_category',
        'image',
        'review',
        'numnber_of_reviews',
        'price',
        'in_stock'
    ]

    list_filter = [
        'category',
        'sub_category',
        'in_stock'
    ]

    search_fields = [
        'name'
    ]



