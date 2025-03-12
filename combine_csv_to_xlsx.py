import os
import re
import pandas as pd

def extract_source_identifier(filename):
    """
    Extracts a numeric identifier from filenames like "group_607317.csv".
    If not found, the filename (without extension) is returned.
    """
    match = re.search(r"group_(\d+)", filename)
    if match:
        return match.group(1)
    return os.path.splitext(filename)[0]

def combine_csv_to_xlsx(input_dir, output_file):
    # List all CSV files in the given input directory.
    csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]
    dataframes = []
    
    for csv_file in csv_files:
        file_path = os.path.join(input_dir, csv_file)
        try:
            # Read CSV with no header (since there is no header row in these files).
            df = pd.read_csv(file_path, header=None)
        except Exception as e:
            print(f"Error reading {csv_file}: {e}")
            continue
        
        # Optionally, add a column to indicate the source file (identifier).
        df['source'] = extract_source_identifier(csv_file)
        dataframes.append(df)
        print(f"Processed file: {file_path}")
    
    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        # Write the combined dataframe to an Excel file with a single sheet.
        combined_df.to_excel(output_file, index=False, sheet_name="Combined")
        print(f"Combined Excel file saved to: {output_file}")
    else:
        print("No CSV files found.")

if __name__ == "__main__":
    input_directory = "final cleaned"  # Folder containing the cleaned CSV files
    output_xlsx = "combined.xlsx"       # Output Excel file path
    combine_csv_to_xlsx(input_directory, output_xlsx)