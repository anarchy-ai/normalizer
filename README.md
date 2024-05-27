# normalizer

We will eventually host this model on HuggingFace at https://huggingface.co/AnarchyAI/normalizer

## Objective

Normalizer is a tool that processes various file types to extract prompt-response pairs for finetuning LLM models on unstructured data.

The end-state will be a GUI where users of any technical level can drag and drop multiple files at once into the application, then they hit a 'create fine-tuning data' button and they'll receive a .csv with a system prompt and a series of matched pair prompt-completion responses.

## Input Formats

- **Text**: .txt, .md, .mdx
- **Documents**: .pdf, .doc, .docx
- **Spreadsheets**: .xlsx, .csv
- **Code**: .py, .js, .html, .java
- **Images**: .jpg, .png (will require OCR)

## Output Format

A .csv file with 3 columns:

| System Prompt                          | User Prompt                           | Response                                     |
| -------------------------------------- | ------------------------------------- | ---------------------------------------------|
| Hi, how can I help you today?          |                                       | 
|                                        | What do these lab results suggest?                          | These lab results suggest that the patient is healthy, as no anomalous data has been detected. |
|                                        | What is the sentiment of the last 5 customers who came into support chat? | The last five customers have a neutral to positive sentiment. |
| | ... | ... |

## Required Libraries

```pip install PyPDF2 python-docx pandas openpyxl pillow pytesseract beautifulsoup4 transformers datasets```

## Project Structure

```CSS
normalizer/
│
├── src/
│   ├── __init__.py
│   ├── file_ingest.py
│   ├── prompt_extractor.py
│   ├── main.py
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```
