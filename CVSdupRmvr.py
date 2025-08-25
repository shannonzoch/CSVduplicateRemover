# -----------------------------------------------------------------------------
# Purpose: This script processes a CSV file by first filtering it to only
#          include rows containing specific keywords ("San Diego" or "La Jolla").
#          It then sorts the remaining data alphabetically based on the values
#          in the first column (Column A) and removes duplicate rows, keeping
#          only the first row for each unique value in that column.
#
# Usage:   python <script_name>.py <input_file.csv> <output_file.csv>
#
# Vibe coded by Shannon Zoch using gemini.
#
# Version History:
#   - v1.2:
#     - Added a pre-processing step to filter rows, keeping only those that
#       contain "San Diego" or "La Jolla" in any column.
#   - v1.1:
#     - Added detailed header comment with purpose, usage, and version tracking.
#     - Modified script to accept input and output file paths as
#       command-line arguments for better reusability.
#     - Removed the automatic creation of a sample 'input.csv'.
#   - v1.0:
#     - Initial script creation.
# -----------------------------------------------------------------------------

import csv
import sys

def process_csv(input_file_path, output_file_path):
    """
    Reads a CSV, filters for specific keywords, sorts by the first column,
    and keeps only the first row for each unique value in the first column.

    Args:
        input_file_path (str): The path to the input CSV file.
        output_file_path (str): The path where the processed CSV file will be saved.
    """
    try:
        # --- 1. Read all rows from the input CSV file ---
        with open(input_file_path, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            # Read header and data separately if a header exists
            try:
                header = next(reader)
                data_rows = list(reader)
                has_header = True
            except StopIteration:
                # This handles the case of an empty file
                header = []
                data_rows = []
                has_header = False

        if not data_rows:
            print("Input CSV file is empty or contains only a header. No data to process.")
            # Create an empty or header-only output file
            with open(output_file_path, mode='w', newline='', encoding='utf-8') as outfile:
                if has_header:
                    writer = csv.writer(outfile)
                    writer.writerow(header)
            return

        # --- 2. Pre-filter rows to keep only those with "San Diego" or "La Jolla" ---
        pre_filtered_rows = []
        for row in data_rows:
            # Join all items in the row into a single string to search for keywords
            row_as_string = ",".join(row)
            if "San Diego" in row_as_string or "La Jolla" in row_as_string:
                pre_filtered_rows.append(row)

        # --- 3. Sort the filtered data rows alphabetically based on the first column ---
        # The key for sorting is the first element (index 0) of each row.
        pre_filtered_rows.sort(key=lambda row: row[0])

        # --- 4. Filter the sorted rows to get the first unique entry per first column value ---
        final_filtered_rows = []
        seen_first_column_values = set()

        for row in pre_filtered_rows:
            # Check if the value in the first column has been seen before
            if row[0] not in seen_first_column_values:
                # If not seen, add the row to our filtered list
                final_filtered_rows.append(row)
                # And add the first column's value to our set of seen values
                seen_first_column_values.add(row[0])

        # --- 5. Write the processed (header + filtered) rows to the output file ---
        with open(output_file_path, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            # Write the header first, if it existed
            if has_header:
                writer.writerow(header)
            # Write the filtered data rows
            writer.writerows(final_filtered_rows)

        print(f"Successfully processed {input_file_path}.")
        print(f"Output saved to {output_file_path}.")

    except FileNotFoundError:
        print(f"Error: The file '{input_file_path}' was not found.")
    except IndexError:
        print("Error: A row in the CSV file appears to be empty or malformed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Main execution block ---
if __name__ == "__main__":
    # Check if the correct number of command-line arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python process_csv.py <input_file.csv> <output_file.csv>")
        sys.exit(1) # Exit the script if arguments are incorrect

    # Get input and output file paths from command-line arguments
    input_csv = sys.argv[1]
    output_csv = sys.argv[2]

    # Call the main processing function with the provided file paths
    process_csv(input_csv, output_csv)
