import os
import PyPDF2
import docx
import pandas as pd
from PIL import Image
import pytesseract
from bs4 import BeautifulSoup

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
        return file.read()

def read_pdf_file(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        for page_num in range(reader.numPages):
            text += reader.getPage(page_num).extractText()
    return text

def read_docx_file(file_path):
    doc = docx.Document(file_path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return '\n'.join(text)


def read_spreadsheet(file_path):
    if file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    else:
        df = pd.read_csv(file_path)
    return df.to_string()

def read_image_file(file_path):
    image = Image.open(file_path)
    return pytesseract.image_to_string(image)

def read_code_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()