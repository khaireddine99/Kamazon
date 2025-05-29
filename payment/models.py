from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from shop.models import Item

class Order(models.Model):
    '''
    Class representing a client order, consists of a group of items and clients info
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    phone_number = PhoneNumberField()

    def __str__(self):
        return f'order {self.id} - {self.email}'

    def get_total_cost(self):
        return sum(item.get_total_price() for item in self.order_items.all())


class OrderItem(models.Model):
    '''
    Class to store the item and quantity belonging to an order

    '''
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.quantity} x {self.item} in order #{self.order.id}'
    
    def get_total_price(self):
        return self.item.price * self.quantity
    




    


