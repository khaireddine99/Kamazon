import os
import csv

# Folder containing your CSV files
folder_path = 'archive'  # <-- Change this to your folder path

# Output file
output_file = 'main.csv'

# Header line to write once
header = ['name', 'main_category', 'sub_category', 'image', 'link', 'ratings', 'no_of_ratings', 'discount_price', 'actual_price']

with open(output_file, mode='w', newline='', encoding='utf-8') as main_csv:
    writer = csv.writer(main_csv)
    writer.writerow(header)  # Write header once

    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, mode='r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header
                for i, row in enumerate(reader):
                    if i >= 20:
                        break
                    writer.writerow(row)
