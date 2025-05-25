import requests
from django.core.management.base import BaseCommand
from shop.models import Item  # Updated import

class Command(BaseCommand):
    help = 'Deletes items with broken image URLs'

    def handle(self, *args, **kwargs):
        broken_count = 0
        total = Item.objects.count()

        self.stdout.write(f'Starting check of {total} items...')

        for index, item in enumerate(Item.objects.all().iterator(), start=1):
            url = item.image  # Updated to use Item.url

            self.stdout.write(f'[{index}/{total}] Checking: {url}')

            try:
                response = requests.head(url, timeout=5)
                if response.status_code >= 400:
                    self.stdout.write(f'❌ Deleting {item} - bad response: {response.status_code}')
                    item.delete()
                    broken_count += 1
            except requests.RequestException as e:
                self.stdout.write(f'❌ Deleting {item} - request error: {e}')
                item.delete()
                broken_count += 1

        self.stdout.write(self.style.SUCCESS(f'✅ Done! Deleted {broken_count} of {total} items.'))
