import json
from langchain_community.llms import Ollama

def load_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

def init_model(model_name):
    return Ollama(base_url="http://localhost:11434", model=model_name)

def generate_prompt(context):
    prompt = (
        "You are a highly accurate text extraction system which will extract questions and answers from completely unstructured data. Your task is to extract the user prompts, and corresponding responses from the given context. Ensure the extracted data follows the exact format given below:\n\n"
        "Format:\n"
        "User Prompt: [question]\n"
        "Response: [response]\n\n"
        "User Prompt: [question]\n"
        "Response: [response]\n\n"
        "...\n\n"
        "Here is the unstructured data:\n"
        f"{context}\n\n"
        "Please follow the exact output format and ensure each user prompt and response is separated by a newline. Only add data that is in the correct format."
    )
    return prompt

def extract_pairs(model, text):
    prompt = generate_prompt(text)
    response = model.invoke(prompt)
    print(response)
    return response

def post_process_response(response):
    pairs = []
    user_prompt = ""
    response_text = ""
    lines = response.split("\n")

    for line in lines:
        line = line.strip()
        if line.startswith("User Prompt:"):
            if user_prompt and response_text:
                pairs.append({"User Prompt": user_prompt, "Response": response_text})
            user_prompt = line.replace("User Prompt:", "").strip()
            response_text = ""
        elif line.startswith("Response:"):
            response_text = line.replace("Response:", "").strip()
    
    if user_prompt and response_text:
        pairs.append({"User Prompt": user_prompt, "Response": response_text})

    return pairs