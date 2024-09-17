import csv
import sys
import os
import asyncio
from typing import List, Tuple, AsyncGenerator
from functools import wraps

class CSVToASCIITable:
    def __init__(self, file_path: str, max_width: int = 30, max_rows: int = None,
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

    @error_handler
    async def read_csv(self) -> AsyncGenerator[List[str], None]:
        async with asyncio.open(self.file_path, 'r', encoding='utf-8') as f:
            content = await f.read()
            reader = csv.reader(content.splitlines(), dialect=self.dialect)
            self.headers = next(reader)
            yield self.headers
            for row in reader:
                yield row

    async def get_max_widths(self, rows: AsyncGenerator[List[str], None]) -> List[int]:
        widths = [min(self.max_width, len(cell)) for cell in self.headers]
        async for row in rows:
            for i, cell in enumerate(row):
                widths[i] = min(self.max_width, max(widths[i], len(cell)))
        return widths

    @staticmethod
    def create_separator(widths: List[int], char: str = '-') -> str:
        return '+' + '+'.join(char * (w + 2) for w in widths) + '+'

    @staticmethod
    def create_row(row: List[str], widths: List[int], align: str = '<') -> str:
        return '|' + '|'.join(f" {cell:{align}{w}} " for cell, w in zip(row, widths)) + '|'

    async def generate_table(self) -> List[str]:
        rows = self.read_csv()
        self.widths = await self.get_max_widths(rows)
        
        separator = self.create_separator(self.widths)
        header_row = self.create_row(self.headers, self.widths, '^')
        
        output = [separator, header_row, separator]
        
        rows = self.read_csv()
        await anext(rows)  # Skip headers
        i = 0
        async for row in rows:
            if self.max_rows and i >= self.max_rows:
                break
            output.append(self.create_row(row, self.widths, self.align))
            i += 1
        
        output.append(separator)
        return output

    async def output_table(self, table: List[str]):
        if self.output_file:
            async with asyncio.open(self.output_file, 'w', encoding='utf-8') as f:
                await f.write('\n'.join(table))
        else:
            print('\n'.join(table))

    @error_handler
    async def run(self):
        table = await self.generate_table()
        await self.output_table(table)

async def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <csv_file_path> [max_width] [max_rows] [align] [output_file]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    max_width = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    max_rows = int(sys.argv[3]) if len(sys.argv) > 3 else None
    align = sys.argv[4] if len(sys.argv) > 4 else '<'
    output_file = sys.argv[5] if len(sys.argv) > 5 else None
    
    converter = CSVToASCIITable(file_path, max_width, max_rows, align, output_file)
    await converter.run()

if __name__ == "__main__":
    asyncio.run(main())