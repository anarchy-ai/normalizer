import os
import re
import PyPDF2
import docx
import pandas as pd
from PIL import Image
import pytesseract
from bs4 import BeautifulSoup
from datetime import datetime

# We need to set the tesseract cmd to the exe file for tesseract
# Instructions for installing tesseract located here: https://github.com/UB-Mannheim/tesseract/wiki
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def infer_datetime_format(date_str):
    possible_formats = [
        '%Y-%m-%d %H:%M:%S',    # Standard format example: '2023-02-28 14:30:00'
        '%Y-%m-%d %H:%M',       # Without seconds: '2023-02-28 14:30'
        '%Y-%m-%d %H:%M:%S.%f', # With microseconds: '2023-02-28 14:30:00.000000'
        '%Y-%m-%d',             # Date only: '2023-02-28'
        '%d-%m-%Y %H:%M:%S',    # European style with day and month swapped: '28-02-2023 14:30:00'
        '%d-%m-%Y %H:%M',       # European style without seconds: '28-02-2023 14:30'
        '%d-%m-%Y',             # European style date only: '28-02-2023'
        '%m-%d-%Y %H:%M:%S',    # Month-day-year format: '02-28-2023 14:30:00'
        '%m-%d-%Y %H:%M',       # Month-day-year format without seconds: '02-28-2023 14:30'
        '%m-%d-%Y',             # Month-day-year format date only: '02-28-2023'
        '%Y/%m/%d %H:%M:%S',    # Standard format with slashes: '2023/02/28 14:30:00'
        '%Y/%m/%d %H:%M',       # Without seconds with slashes: '2023/02/28 14:30'
        '%Y/%m/%d %H:%M:%S.%f', # With microseconds with slashes: '2023/02/28 14:30:00.000000'
        '%Y/%m/%d',             # Date only with slashes: '2023/02/28'
        '%d/%m/%Y %H:%M:%S',    # European style with day and month swapped and slashes: '28/02/2023 14:30:00'
        '%d/%m/%Y %H:%M',       # European style without seconds and slashes: '28/02/2023 14:30'
        '%d/%m/%Y',             # European style date only with slashes: '28/02/2023'
        '%m/%d/%Y %H:%M:%S',    # Month-day-year format with slashes: '02/28/2023 14:30:00'
        '%m/%d/%Y %H:%M',       # Month-day-year format without seconds with slashes: '02/28/2023 14:30'
        '%m/%d/%Y',             # Month-day-year format date only with slashes: '02/28/2023'
    ]

    for date_format in possible_formats:
        try:
            datetime.strptime(date_str, date_format)
            return date_format
        except ValueError:
            continue
    
    # If no format matches
    raise ValueError("Could not infer datetime format from input string")

def read_file(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    
    if extension == '.txt':
        return read_text_file(file_path)
    elif extension == '.pdf':
        return read_pdf_file(file_path)
    elif extension == '.docx':
        return read_docx_file(file_path)
    elif extension in ['.xlsx', '.csv']:
        return read_spreadsheet(file_path)
    elif extension in ['.jpg', '.png']:
        return read_image_file(file_path)
    elif extension in ['.py', '.js', '.html', '.java']:
        return read_code_file(file_path)
    else:
        raise ValueError(f"Unsupported file type: {extension}")

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        paragraphs = content.split('\n\n')
        text = [para.strip() for para in paragraphs if para.strip()]
        ### DEBUG ONLY ###
        for para in text:
            print(para + "\n")
    
    return text

def read_pdf_file(file_path):
    text = []
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page_text = reader.pages[page_num].extract_text()
            print(page_text)
            text.append(page_text)
    return text

def read_docx_file(file_path):
    doc = docx.Document(file_path)
    text = []
    for para in doc.paragraphs:
        ### DEBUG ONLY ###
        print(para.text + "\n")
        ##################
        text.append(para.text)
    return text

def read_excel(file_path):
    return pd.read_excel(file_path)

def read_csv(file_path):
    return pd.read_csv(file_path)

# Functions to compute statistics for different datatypes
def get_numeric_stats(col_data):
    return {
        'mean': col_data.mean(),
        'median': col_data.median(),
        'std': col_data.std(),
        'min': col_data.min(),
        'max': col_data.max(),
        '25th_percentile': col_data.quantile(0.25),
        '75th_percentile': col_data.quantile(0.75),
        'sum': col_data.sum(),
        'count': col_data.count(),
        'variance': col_data.var()
    }

def get_string_stats(col_data):
    return {
        'mode': col_data.mode()[0] if not col_data.mode().empty else None,
        'unique_count': col_data.nunique(),
        'total_length': col_data.str.len().sum(),
        'mean_length': col_data.str.len().mean(),
        'max_length': col_data.str.len().max(),
        'min_length': col_data.str.len().min(),
        'most_frequent': col_data.value_counts().idxmax() if not col_data.value_counts().empty else None,
        'least_frequent': col_data.value_counts().idxmin() if not col_data.value_counts().empty else None,
        'frequency_distribution': col_data.value_counts().to_dict(),
        'unique_values': col_data.unique()
    }

def get_datetime_stats(col_data):
    return {
        'min_date': col_data.min(),
        'max_date': col_data.max(),
        'range': col_data.max() - col_data.min(),
        'median_date': col_data.median(),
        'start_year': col_data.min().year,
        'end_year': col_data.max().year,
        'start_month': col_data.min().month,
        'end_month': col_data.max().month,
        'start_day': col_data.min().day,
        'end_day': col_data.max().day
    }

def get_boolean_stats(col_data):
    # Ensure col_data is treated as a numeric array
    col_data_numeric = col_data.astype(int)
    return {
        'count_true': col_data.sum(),
        'count_false': col_data.count() - col_data.sum(),
        'percent_true': col_data.mean() * 100,
        'percent_false': (1 - col_data.mean()) * 100,
        'unique_count': col_data.nunique(),
        'mode': col_data.mode()[0] if not col_data.mode().empty else None,
        'most_frequent': col_data.value_counts().idxmax() if not col_data.value_counts().empty else None,
        'least_frequent': col_data.value_counts().idxmin() if not col_data.value_counts().empty else None,
        'frequency_distribution': col_data.value_counts().to_dict()
    }

def read_spreadsheet(file_path):
    if file_path.endswith('.xlsx'):
        df = read_excel(file_path)
    else:
        df = read_csv(file_path)
    
    stats = []
    for column in df.columns:
        col_data = df[column]
        
        # Check if the column is boolean (including strings 'True'/'False' or 'true'/'false')
        if _is_boolean_dtype(col_data):
            col_stats = get_boolean_stats(col_data)
            col_type = col_data.dtype
        
        # Check if the column is datetime (including strings that can be parsed as datetime)
        elif _is_datetime_dtype(col_data):
            col_data = pd.to_datetime(col_data, errors='coerce', infer_datetime_format=True)  # Convert to datetime, coerce errors
            col_data = col_data.dropna()  # Drop NaT (Not a Time) values after conversion
            
            col_stats = get_datetime_stats(col_data)
            col_type = col_data.dtype
        
        # Check if the column is numeric
        elif pd.api.types.is_numeric_dtype(col_data):
            col_stats = get_numeric_stats(col_data)
            col_type = col_data.dtype
        
        # Default to string type if none of the above matched
        else:
            col_stats = get_string_stats(col_data)
            col_type = col_data.dtype

        for stat_name, stat_value in col_stats.items():
            stat_str = (f"File: {os.path.basename(file_path)}, "
                        f"Column: {column}, "
                        f"Type: {col_type}, "
                        f"{stat_name}: {stat_value}")
            stats.append(stat_str)

    return stats

def _is_boolean_dtype(col_data):
    if col_data.dtype.name == 'bool':
        return True
    elif pd.api.types.is_string_dtype(col_data):
        # Check if all string values can be interpreted as boolean
        return col_data.apply(lambda x: x.lower() in ['true', 'false']).all()
    else:
        return False

def _is_datetime_dtype(col_data):
    if pd.api.types.is_string_dtype(col_data):
        # Attempt to parse strings as datetime, handling multiple formats
        for date_str in col_data:
            try:
                infer_datetime_format(date_str)
            except ValueError:
                return False
        return True
    else:
        return False

def read_image_file(file_path):
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    paragraphs = text.split('\n\n')
    paragraph_list = [para.strip() for para in paragraphs if para.strip()]
    return paragraph_list

def read_code_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # Normalize newlines
    content = content.replace('\r\n', '\n').replace('\r', '\n')

    # Split content into blocks based on multiple newlines
    blocks = content.split('\n\n')

    # Strip leading and trailing whitespace from each block
    blocks = [block.strip() for block in blocks if block.strip()]
    for block in blocks:
        print(block)

    return blocks
