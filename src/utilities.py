import pandas as pd
import os
def save_to_csv(data, output_path):
    # Prepare rows to append
    rows = [{"User Prompt": pair["User Prompt"], "Response": pair["Response"]} for pair in data]
    
    # Convert rows to DataFrame
    df = pd.DataFrame(rows)
    
    # Append to CSV file
    if not os.path.isfile(output_path):
        df.to_csv(output_path, index=False)
    else:
        df.to_csv(output_path, mode='a', header=False, index=False)
