# custom management command to add slug fields to items
from django.core.management.base import BaseCommand
from shop.models import Item
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Populate missing slugs for Items'

    def handle(self, *args, **kwargs):
        items = Item.objects.all()
        updated = 0
        for item in items:
            if not item.slug:
                first_word = item.name.split()[0]
                item.slug = f"{item.id}-{slugify(first_word)}"
                item.save(update_fields=["slug"])
                updated += 1
        self.stdout.write(f"Updated {updated} items with slugs.")
