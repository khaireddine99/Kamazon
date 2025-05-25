import os

# Change this to the path of your folder
folder_path = r'archive'

# List all files that end with .csv
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

total_num_lines = 0

for file in csv_files:
    file_path = os.path.join(folder_path, file)
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        # Subtract 1 if the first line is a header
        num_lines = len(lines) - 1
        total_num_lines += num_lines
        print(f'{num_lines}')

print(f'total number of lines {total_num_lines}')