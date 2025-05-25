from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from shop.models import Item
from .cart import Cart

# Create your views here.
def index(request):
    return render(request, 'cart.html')

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Item, id=product_id)
    cart.add(product=product, quantity=1)
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Item, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})
