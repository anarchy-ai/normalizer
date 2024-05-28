import argparse
import os
from .file_ingest import read_file
from .prompt_extractor import load_config, init_model, extract_pairs, post_process_response
from .utilities import save_to_csv

def main(input_file, output_file):
    model_name = "llama3"
    model = init_model(model_name)
    
    try:
        content = read_file(input_file)
        if content:
            response = extract_pairs(model, content)
            system_prompt, pairs = post_process_response(response)
            save_to_csv(system_prompt, pairs, output_file)
            print(f"Prompt-response pairs extracted and saved to {output_file}")
        else:
            print("No content found in the file.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract prompt-response pairs from various file types.")
    parser.add_argument('--input_file', type=str, required=True, help="Path to the input file.")
    parser.add_argument('--output_file', type=str, required=True, help="Path to save the output CSV file.")
    
    args = parser.parse_args()
    main(args.input_file, args.output_file)


