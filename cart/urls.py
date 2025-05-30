from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.index, name='index'),
    path('cart_details/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/<int:product_id>/', views.cart_update, name='cart_update'),
]