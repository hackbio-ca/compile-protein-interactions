"""
Script: process_abstracts.py

Description:
This script reads a plain text file containing scientific abstracts (e.g., from PubMed), 
processes the text, and saves the results as a CSV file. The script is designed to be 
flexible and accepts input and output file paths as command-line arguments.

Key Features:
1. Reads a text file containing multiple abstracts.
2. Can be adapted to parse and extract specific information (e.g., PMID, abstract text).
3. Saves the processed data in CSV format for downstream analysis.
4. Optional: Can be extended to save data in JSON format.

Usage:
python process_abstracts.py -i /path/to/input.txt -o /path/to/output.csv

Arguments:
-i, --input   : Path to the input text file containing abstracts.
-o, --output  : Path to save the output CSV file.
"""

import pandas as pd 
import arg
import os 
import re 
import json
import argparse

# --- Argument Parser ---
parser = argparse.ArgumentParser(description="Process abstracts and save as CSV")
parser.add_argument(
    "-i", "--input", type=str, required=True,
    help="Path to the input text file containing abstracts"
)
parser.add_argument(
    "-o", "--output", type=str, required=True,
    help="Path to save the output CSV file"
)

args = parser.parse_args()
data_path = args.input
csv_path = args.output

# --- Reading Data ---
with open(data_path, "r", encoding="utf-8") as f:
    text = f.read()
# print(text[:500])  # first 500 characters

# --- Extracting inforamtion ---
articles = re.split(r'\n\s*\n\s*\n', text)  # split on 2 or more consecutive blank lines

pmid_to_abstract = {}
skipped_no_pmid = 0
skipped_no_abstract = 0
skipped_short_abstract = 0
captured = 0

for i, art in enumerate(articles[1:], start=1):  # start=1 so the first article is 1

    print(f"Reading article {i}...")
    
    # Find PMID anywhere in the article
    pmid_match = re.search(r'PMID:\s*(\d+)', art)
    if not pmid_match:
        skipped_no_pmid += 1
        print(f"No PMID found for article {i}, skipping.")
        continue
    pmid = pmid_match.group(1)

    # # Handle "Update of" special case
    # update_of_match = re.search(r'Update of.*?\n\s*\n', art, re.IGNORECASE)
    # start_pos = update_of_match.end() if update_of_match else 0
    # art_for_abstract = art[start_pos:]

    # Extract abstract
    abstract_match = re.search(
        r'Author information:.*?\n(?:[^\S\n]*\S.*?\n)*\n(.*?)(?=\n\s*\n)',
        art,
        re.DOTALL | re.IGNORECASE
    )

    if not abstract_match:
        skipped_no_abstract += 1
        print(f"No author information or abstract found for PMID {pmid}, skipping.")
        continue

    # abstract_lines = [line.strip() for line in abstract_match.group(1).split('\n') if line.strip()]
    
    # if len(abstract_lines) < 3:
    #     skipped_short_abstract += 1
    #     print(f"Abstract too short for PMID {pmid}, skipping.")
    #     continue

    abstract = ' '.join(abstract_match.group(1).split())
    pmid_to_abstract[pmid] = abstract
    captured += 1
    print(f"Article {i} (PMID {pmid}) abstract captured.")

# Inspect the dictionary
total_entries = len(pmid_to_abstract)
empty_pmids = sum(1 for k in pmid_to_abstract.keys() if not str(k).strip())
empty_abstracts = sum(1 for v in pmid_to_abstract.values() if not v.strip())

print(f"Total entries in pmid_to_abstract: {total_entries}")
print(f"Entries with empty PMID: {empty_pmids}")
print(f"Entries with empty abstract: {empty_abstracts}")

# # --- Preview results ---
# for pmid, abstract in pmid_to_abstract.items():
#     print(f"PMID: {pmid}\nAbstract: {abstract[:1000]}...\n")  # first 200 chars

# --- Creating dataframe ---
df = pd.DataFrame(list(pmid_to_abstract.items()), columns=["PMID", "Abstract"])
print("QC OF PANDAS DF")
print(df.head())
print(len(df))
# print(df)

# --- Saving as .json file ---
json_path = '/Users/marlenfaf/Desktop/TBH_2025/pmid_to_abstract.json'
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(pmid_to_abstract, f, ensure_ascii=False, indent=4)
print(f"Dictionary saved as JSON to {json_path}")
