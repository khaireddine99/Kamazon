from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='base'),
    path('shop', views.shop_items, name='shop_items')
]