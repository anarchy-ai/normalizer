import pandas as pd

def save_to_csv(system_prompt, data, output_path):
    rows = [{"System Prompt": system_prompt, "User Prompt": "", "Response": ""}]
    for pair in data:
        rows.append({"System Prompt": "", "User Prompt": pair["User Prompt"], "Response": pair["Response"]})
    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
