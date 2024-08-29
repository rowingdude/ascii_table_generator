import csv
import sys

def read_csv(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        data = list(reader)
    return headers, data

def get_max_widths(headers, data):
    widths = [len(h) for h in headers]
    for row in data:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))
    return widths

def create_separator(widths):
    return '+' + '+'.join('-' * (w + 2) for w in widths) + '+'

def create_header_row(headers, widths):
    return '|' + '|'.join(f' {h.center(w)} ' for h, w in zip(headers, widths)) + '|'

def create_data_row(row, widths):
    return '|' + '|'.join(f' {cell.ljust(w)} ' for cell, w in zip(row, widths)) + '|'

def generate_ascii_table(file_path):
    headers, data = read_csv(file_path)
    widths = get_max_widths(headers, data)
    
    separator = create_separator(widths)
    header_row = create_header_row(headers, widths)
    
    print(separator)
    print(header_row)
    print(separator)
    
    for row in data:
        print(create_data_row(row, widths))
    
    print(separator)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <csv_file_path>")
        sys.exit(1)
    
    generate_ascii_table(sys.argv[1])