from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('', views.index, name='index'),
    path('create_order', views.create_order, name='create_order'),
    path('process', views.process_payment, name='process'),
    path('completed', views.payment_completed, name='completed'),
    path('canceled', views.payment_canceled, name='canceled')
]