import stripe
from django.conf import settings  # ✅ Import from Django settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

stripe.api_key = settings.STRIPE_SECRET_KEY  # ✅ Use what's in settings

def index(request):
    return render(request, 'payment/index.html')
