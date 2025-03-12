import os
import pandas as pd

def group_to_csv(input_file, output_dir):
    # Create output directory if it doesn't exist.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read the 'Processed' worksheet without headers and skip the first row.
    df = pd.read_excel(input_file, sheet_name='Processed', header=None, skiprows=1)

    # Group by column C (index 2)
    groups = df.groupby(2)

    for name, group in groups:
        # Sanitize the group name to create a valid file name.
        safe_name = str(name).strip().replace(" ", "_")
        # Construct output file path.
        output_file = os.path.join(output_dir, f"group_{safe_name}.csv")
        # Write the group to CSV; index and header are omitted.
        group.to_csv(output_file, index=False, header=False)
        print(f"Group '{name}' written to: {output_file}")

if __name__ == "__main__":
    input_excel = "LibE2025dev.xlsx"  # Input file
    output_directory = "grouped_csvs"  # Output directory for CSV files
    group_to_csv(input_excel, output_directory)