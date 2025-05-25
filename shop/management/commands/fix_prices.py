from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Divide all item prices by 100 and round to 2 decimal places'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute('UPDATE shop_item SET price = ROUND(price / 100.0,  2);')
        self.stdout.write(self.style.SUCCESS("✅ Prices updated successfully."))

