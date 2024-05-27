from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from src.file_ingest import read_file
from src.prompt_extractor import extract_pairs, save_to_csv

app = FastAPI()

@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    content = await file.read()
    text = read_file(content)
    if text:
        pairs = extract_pairs(text)
        output_path = "output.csv"
        save_to_csv(pairs, output_path)
        return JSONResponse(content={"message": "Extraction successful", "output_file": output_path})
    else:
        return JSONResponse(content={"message": "Failed to read file"}, status_code=400)