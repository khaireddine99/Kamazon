import stripe
from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from cart.cart import Cart
from .forms import OrderForm
from .models import OrderItem, Order
from shop.utils.recommendation import update_recommendations
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.mail import send_mail
from datetime import date, timedelta

stripe.api_key = settings.STRIPE_SECRET_KEY  # ✅ Use what's in settings

def index(request):
    return render(request, 'payment/index.html')

def create_order(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            print("order form is valid")
            order = form.save(commit=False)
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    item=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )

            items_bought_together = [int(item.item.id) for item in order.items.all()]
            update_recommendations(items_bought_together)

            cart.clear()
            request.session['order_id'] = order.id
            
            return redirect('payment:process')

        else:
            print("order form is invalid")
            form.add_error(None, 'Invalid reCAPTCHA. Please try again.')
            # Do NOT redirect here; let the code fall through to re-render the form

    else:
        form = OrderForm()

    # Render the form with errors if any
    return render(request, 'payment/create_order.html', {'cart': cart, 'form': form})


def process_payment(request):
    '''
    payment view, redirects the user to a STRIPE payment page
    '''
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    items = order.items.all()

    if request.method == 'POST':
        success_url = request.build_absolute_uri(
            reverse('payment:completed')
        )
    
        cancel_url = request.build_absolute_uri(
            reverse('payment:canceled')
        )

        session_data = {
            'mode':'payment',
            'client_reference_id':order.id,
            'success_url':success_url,
            'cancel_url':cancel_url,
            'metadata': {
                'order_id': str(order.id)
            },
            'line_items':[]
        }

        for item in order.items.all():
            session_data['line_items'].append(
                {
                    'price_data':{
                            'unit_amount': int(item.price * Decimal('100')),
                            'currency':'usd',
                            'product_data':{
                                'name':item.item.name,
                            },
                        },
                    'quantity': item.quantity
                }
            )

        session = stripe.checkout.Session.create(**session_data)
        return redirect(session.url, code=303)

    else:
        context = {
            'items':items,
            'order':order
        }
        
        return render(request, 'payment/process.html', context)

def payment_completed(request):
    return render(request, 'payment/completed.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')

@csrf_exempt
def stripe_webhook(request):
    '''
    Stripe webhook view, notify when an order is paid
    '''
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session.get('metadata', {}).get('order_id')

        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                order.paid = True
                order.save()

                # send an email to the client after the order has been paid
                today = date.today()
                formatted_date = today.strftime("%B %d, %Y")
                eta_date = today + timedelta(days=3)
                formatted_eta_date = eta_date.strftime("%B %d, %Y")

                send_mail(
                    subject='Thank you for shopping with Kamazon',
                    message=f'Your order has been paid, it cost {order.get_total_cost()}$, payment happened at {formatted_date}, your order will be delivered to {order.address} at {formatted_eta_date}',
                    from_email='khairisigma@gmail.com',
                    recipient_list=[order.email],
                    fail_silently=False,
                )
       
            except Order.DoesNotExist:
                pass

    return HttpResponse(status=200)
