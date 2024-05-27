import json
from langchain_community.llms import Ollama

def load_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

def init_model(model_name):
    return Ollama(base_url="http://localhost:11434", model=model_name)

def generate_prompt(context):
    prompt = (
        "You are a highly accurate text extraction system which will extract data from completely unstructured data and you are smart enough, to generate the pairs. So, this data can be used to finetuned other models. and give me the the below format. Your task is to extract the system prompt, user prompts, and corresponding responses from the given conversation. If there is no system prompt, please indicate 'not found'. Ensure the extracted data is complete and follows the exact format given below:\n\n"
        "Format:\n"
        "System Prompt: [from unstructured data]\n"
        "User Prompt: [from unstructured data]\n"
        "Response: [from unstructured data]\n\n"
        "User Prompt: [from unstructured data]\n"
        "Response: [from unstructured data]\n\n"
        "...\n\n"
        "Here is the unstructured data:\n"
        f"{context}\n\n"
        "Please follow the exact output format and ensure each user prompt and response is separated by a newline."
    )
    return prompt

def extract_pairs(model, text):
    prompt = generate_prompt(text)
    response = model.invoke(prompt)
    return response

def post_process_response(response):
    pairs = []
    system_prompt = "not found"
    user_prompt = ""
    response_text = ""
    lines = response.split("\n")
    first_machine_response = True

    for line in lines:
        line = line.strip()
        if line.startswith("System Prompt:"):
            system_prompt = line.replace("System Prompt:", "").strip()
            if system_prompt.lower() == "not found":
                system_prompt = None
        elif line.startswith("User Prompt:"):
            if user_prompt and response_text:
                pairs.append({"User Prompt": user_prompt, "Response": response_text})
            user_prompt = line.replace("User Prompt:", "").strip()
            response_text = ""
        elif line.startswith("Response:"):
            response_text = line.replace("Response:", "").strip()
            if first_machine_response and system_prompt == "not found":
                system_prompt = response_text
                first_machine_response = False
        elif line.lower() == "not found":
            system_prompt = "not found"

    if user_prompt and response_text:
        pairs.append({"User Prompt": user_prompt, "Response": response_text})

    return system_prompt, pairs