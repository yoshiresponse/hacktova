import os
from google import genai

def extract_csv(text):
    """
    If the returned text is wrapped in markdown code blocks (e.g. ```csv ... ```),
    remove them and return just the CSV text.
    """
    text = text.strip()
    if text.startswith("```") and text.endswith("```"):
        lines = text.splitlines()
        if len(lines) >= 3:
            # Remove the first and last lines (fence and language hint)
            text = "\n".join(lines[1:-1])
        else:
            text = text.strip("`")
    return text

def extract_candidate_text(candidate):
    """
    Extract text from a candidate. If the candidate has a 'text' attribute, use it.
    Otherwise, if it has 'parts', combine the text from each part.
    """
    if hasattr(candidate, "text") and candidate.text:
        return candidate.text
    elif hasattr(candidate, "parts"):
        texts = []
        for part in candidate.parts:
            if hasattr(part, "text") and part.text:
                texts.append(part.text)
        if texts:
            return "\n".join(texts)
    return str(candidate)

def send_csv_to_gemini(api_key, csv_text):
    # Create a client using your API key.
    client = genai.Client(api_key=api_key)

    prompt = "Add an example value to each line/row of the csv."
    # Combine prompt and CSV text so that the model knows what to do.
    contents = f"{prompt}\n\n{csv_text}"

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=contents,
    )

    # Look for a proper result in response.result; otherwise check candidates.
    if not hasattr(response, "result") or not response.result:
        if hasattr(response, "candidates") and response.candidates:
            candidate = response.candidates[0].content
            candidate_text = extract_candidate_text(candidate)
            return extract_csv(candidate_text)
        else:
            raise Exception("Gemini API error: " + str(response))
    else:
        return extract_csv(response.result)

def process_csv_files(input_dir, output_dir, api_key):
    # Create the output directory if it doesn't exist.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process each CSV file in the input directory.
    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            input_file = os.path.join(input_dir, filename)
            with open(input_file, "r") as f:
                csv_text = f.read()
            print(f"Processing file: {input_file}")

            try:
                updated_csv = send_csv_to_gemini(api_key, csv_text)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue

            # Save the extracted CSV to the output directory.
            output_file = os.path.join(output_dir, filename)
            with open(output_file, "w") as f:
                f.write(updated_csv)
            print(f"Updated CSV saved to: {output_file}")

if __name__ == "__main__":
    input_dir = "grouped_csvs"      # Folder containing the original CSV files
    output_dir = "gemini_output"     # Folder where updated CSV files will be saved
    api_key = "AIzaSyDwqwiqRKspy2v8X_mbMdNzjVhnV1bDwNQ"  # Replace with your Gemini API key

    process_csv_files(input_dir, output_dir, api_key)