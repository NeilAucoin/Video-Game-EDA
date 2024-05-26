# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 11:04:44 2024

@author: neila
"""

import os
import json
import csv

#%% Combine .json files into a csv

def json_to_csv(json_dir, csv_file):
    # Open CSV file for writing
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'slug', 'name', 'released', 'tba', 'background_image', 'rating', 'rating_top',
                      'ratings', 'ratings_count', 'reviews_text_count', 'added', 'metacritic',
                      'playtime', 'suggestions_count', 'updated', 'user_game', 'reviews_count', 'community_rating',
                      'saturated_color', 'dominant_color', 'platforms', 'parent_platforms', 'genres', 'stores',
                      'clip', 'tags', 'esrb_rating', 'short_screenshots', 'added_by_status.owned']
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Counter for tracking processed files
        file_counter = 0
        
        # Loop through each JSON file in the directory
        for filename in os.listdir(json_dir):
            if filename.endswith('.json'):
                file_counter += 1
                print(f"Processing file {file_counter}")

                # Read JSON file
                with open(os.path.join(json_dir, filename), 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON in file {filename}: {e}")
                        continue

                # Initialize row dictionary
                row = {}
                
                # Populate row with data from JSON
                for field in fieldnames:
                    if "." in field:
                        nested_fields = field.split(".")
                        nested_data = data.get(nested_fields[0], {})
                        if nested_data is not None:
                            row[field] = nested_data.get(nested_fields[1], None)
                        else:
                            row[field] = None
                    else:
                        row[field] = data.get(field, None)
                
                writer.writerow(row)

# Directory containing JSON files
json_dir = r"C:\Users\Niocu\OneDrive\Data Science\ds-final-project-main\data"
# Output CSV file
csv_file = r"C:\Users\Niocu\OneDrive\Data Science\ds-final-project-main\data\final_new_data.csv"

# Run code
json_to_csv(json_dir, csv_file)

