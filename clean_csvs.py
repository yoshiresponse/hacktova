import os

def clean_csv(file_content):
    """
    Extracts only the raw CSV data from a Gemini response file.
    It looks for a fenced code block starting with a line that begins with "```csv"
    and ends with a line that starts with "```". Only the lines in between are kept.
    If no such fenced block is found, it returns an empty string.
    """
    lines = file_content.splitlines()
    inside_csv_block = False
    csv_lines = []
    for line in lines:
        stripped = line.strip()
        # Start capturing when the fence with csv is found.
        if not inside_csv_block and stripped.lower().startswith("```csv"):
            inside_csv_block = True
            continue  # Skip the opening fence
        # End capturing when closing fence is reached.
        if inside_csv_block and stripped.startswith("```"):
            inside_csv_block = False
            break
        if inside_csv_block:
            # Only record nonempty lines
            if stripped:
                csv_lines.append(line)
    return "\n".join(csv_lines)

def process_csv_files(input_dir, output_dir):
    # Create the output directory if it doesn't exist.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process each file in the input directory.
    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            input_file = os.path.join(input_dir, filename)
            with open(input_file, "r", encoding="utf-8") as f:
                content = f.read()
            print(f"Processing file: {input_file}")

            cleaned_csv = clean_csv(content)
            if not cleaned_csv:
                print(f"No CSV block found in {filename}, skipping.")
                continue

            output_file = os.path.join(output_dir, filename)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(cleaned_csv)
            print(f"Cleaned CSV saved to: {output_file}")

if __name__ == "__main__":
    input_directory = "gemini_output"   # Folder containing the Gemini output CSV files
    output_directory = "cleaned_csv"    # Folder where the cleaned CSV files will be saved
    process_csv_files(input_directory, output_directory)