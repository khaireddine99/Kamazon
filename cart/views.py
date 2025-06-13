from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from shop.models import Item
from .cart import Cart
from django.http import HttpResponseRedirect
from shop.utils.recommendation import get_combined_recommendations

# Create your views here.
def index(request):
    return render(request, 'cart.html')

from django.shortcuts import get_object_or_404, redirect
from shop.models import Item
from .cart import Cart

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Item, id=product_id)

    try:
        quantity = int(request.POST.get("quantity", 1))
        if quantity < 1:
            quantity = 1
    except (ValueError, TypeError):
        quantity = 1

    cart.add(product=product, quantity=quantity)
    messages.success(request, 'Item added to the cart')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Item, id=product_id)
    cart.remove(product)
    messages.success(request, 'Item removed from the cart')
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)

    # recommend items based on the items existing in the cart
    item_ids = cart.keys()
    recommended_items_ids = get_combined_recommendations(item_ids)
    recommended_items = Item.objects.filter(id__in=recommended_items_ids)

    # recommend more items if the recommended items are less than 5
    if len(recommended_items_ids) < 5:
        additional_items_needed = 5 - len(recommended_items_ids)
        additional_items = Item.objects.exclude(id__in=recommended_items_ids).filter(category='stores')[:additional_items_needed]
        all_recommended_items = list(recommended_items) + list(additional_items)
        recommended_items = all_recommended_items

    return render(request, 'cart/detail.html', {'cart': cart, 'recommended_items':recommended_items})

@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Item, id=product_id)
    
    try:
        quantity = int(request.POST.get("quantity", 1))
        if quantity < 1:
            quantity = 1
    except (ValueError, TypeError):
        quantity = 1

    cart.add(product=product, quantity=quantity, override_quantity=True)
    messages.success(request, 'Cart updated.')
    return redirect('cart:cart_detail')
