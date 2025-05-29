from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('', views.create_checkout_session, name='index')
]