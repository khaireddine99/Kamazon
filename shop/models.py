from django.db import models


class Item(models.Model):
    '''
    Item model class
    '''
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    image = models.URLField(max_length=500)
    review = models.FloatField()
    numnber_of_reviews = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.name 

