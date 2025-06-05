from django.db import models
from django.utils.text import slugify


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
    slug = models.SlugField(max_length=120, blank=True)

    def save(self, *args, **kwargs):
        # Save first to get an ID (only if the object is new and has no slug)
        if not self.slug:
            super().save(*args, **kwargs)
            first_word = self.name.split()[0]
            self.slug = f"{self.id}-{slugify(first_word)}"
            return super().save(update_fields=["slug"])
        else:
            return super().save(*args, **kwargs)

    def __str__(self):
        return self.name 

