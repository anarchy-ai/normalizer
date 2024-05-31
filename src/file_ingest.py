import os
import re
import PyPDF2
import docx
import pandas as pd
from PIL import Image
import pytesseract
from bs4 import BeautifulSoup

# We need to set the tesseract cmd to the exe file for tesseract
# Instructions for installing tesseract located here: https://github.com/UB-Mannheim/tesseract/wiki
pytesseract.pytesseract.tesseract_cmd =r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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


def read_spreadsheet(file_path):
    if file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    else:
        df = pd.read_csv(file_path)
    return df.to_string()

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
    
