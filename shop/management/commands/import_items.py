import csv
from django.core.management.base import BaseCommand
from shop.models import Item

class Command(BaseCommand):
    help = 'Import items from a CSV file into the Item model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
    
    def clean_price(self, price_str):
        # Remove any currency symbols and commas
        return float(price_str.replace('₹', '').replace(',', '').strip())

    def clean_int(self, value):
        return int(value.replace(',', '').strip())

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                try:
                    Item.objects.create(
                        name=row['name'],
                        category=row['main_category'],
                        sub_category=row['sub_category'],
                        image=row['image'],
                        review=float(row['ratings']),
                        numnber_of_reviews=self.clean_int(row['no_of_ratings']),
                        price=self.clean_price(row['discount_price']),
                        in_stock=True
                    )
                    count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed on row: {row}\n{e}"))
            self.stdout.write(self.style.SUCCESS(f"Successfully imported {count} items"))