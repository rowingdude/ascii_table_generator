import csv
import sys
import os
import asyncio
from typing import List, Tuple, AsyncGenerator
from functools import wraps

class CSVToASCIITable:
    def __init__(self, file_path: str, max_width: int = None, max_rows: int = None,
                 align: str = '<', output_file: str = None, dialect: str = 'excel'):
        self.file_path = file_path
        self.max_width = max_width
        self.max_rows = max_rows
        self.align = align
        self.output_file = output_file
        self.dialect = dialect
        self.headers = []
        self.widths = []

    @staticmethod
    def error_handler(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except FileNotFoundError:
                print(f"Error: File '{args[0].file_path}' not found.")
                sys.exit(1)
            except csv.Error as e:
                print(f"Error reading CSV file: {e}")
                sys.exit(1)
        return wrapper

    async def read_csv(self) -> AsyncGenerator[List[str], None]:
        with open(self.file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f, dialect=self.dialect)
            self.headers = next(reader)
            yield self.headers
            for row in reader:
                yield row

    async def get_max_widths(self) -> List[int]:
        widths = [len(cell) for cell in self.headers]
        max_columns = len(self.headers)
        async for row in self.read_csv():
            max_columns = max(max_columns, len(row))
            for i, cell in enumerate(row):
                if i >= len(widths):
                    widths.append(len(cell))
                else:
                    widths[i] = max(widths[i], len(cell))
        
        # Pad headers if necessary
        self.headers.extend([''] * (max_columns - len(self.headers)))
        
        # Apply max_width if specified
        if self.max_width:
            widths = [min(w, self.max_width) for w in widths]
        
        return widths

    @staticmethod
    def create_separator(widths: List[int], char: str = '-') -> str:
        return '+' + '+'.join(char * (w + 2) for w in widths) + '+'

    @staticmethod
    def create_row(row: List[str], widths: List[int], align: str = '<') -> str:
        return '|' + '|'.join(f" {cell:{align}{w}} " for cell, w in zip(row, widths)) + '|'

    async def generate_table(self) -> AsyncGenerator[str, None]:
        self.widths = await self.get_max_widths()
        
        separator = self.create_separator(self.widths)
        header_row = self.create_row(self.headers, self.widths, '^')
        
        yield separator
        yield header_row
        yield separator
        
        i = 0
        async for row in self.read_csv():
            if row == self.headers:
                continue
            if self.max_rows and i >= self.max_rows:
                break
            # Pad row if necessary
            row.extend([''] * (len(self.widths) - len(row)))
            yield self.create_row(row, self.widths, self.align)
            i += 1
        
        yield separator

    async def output_table(self):
        if self.output_file:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                async for line in self.generate_table():
                    f.write(line + '\n')
        else:
            async for line in self.generate_table():
                print(line)

    @error_handler
    async def run(self):
        await self.output_table()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <csv_file_path> [max_width] [max_rows] [align] [output_file]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    max_width = int(sys.argv[2]) if len(sys.argv) > 2 else None
    max_rows = int(sys.argv[3]) if len(sys.argv) > 3 else None
    align = sys.argv[4] if len(sys.argv) > 4 else '<'
    output_file = sys.argv[5] if len(sys.argv) > 5 else None
    
    converter = CSVToASCIITable(file_path, max_width, max_rows, align, output_file)
    await converter.run()

if __name__ == "__main__":
    asyncio.run(main())
