import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import OrderForm
from .models import OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY  # ✅ Use what's in settings

def index(request):
    return render(request, 'payment/index.html')

def create_order(request):
    # create the cart
    cart = Cart(request)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            for item in cart:
                print(item)
                OrderItem.objects.create(
                    order=order,
                    item=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
        
        cart.clear()
        request.session['order_id'] = order.id

        return redirect('payment:process')
    else:
        form = OrderForm()
    
    return render(
        request,
        'payment/create_order.html',
        {'cart':cart, 'form':form}
    )

def process_payment(request):
    return render(request, 'payment/process.html')