# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 12:41:57 2024

@author: NeilLaptop
"""

API_KEY = 'XXX'

import requests
import json
import time
import os
import re
import csv

#%% Initial Scraper

BASE_URL = 'https://api.rawg.io/api/'
endpoint = 'games'
params = {
    'page_size': 100,
    'ordering': '-added',
    'key': API_KEY,
    'page': 0
    }

# Function to replace invalid characters
def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*,.)()]', '_', name)

def fetch_and_save_data(file_path):
    all_games_data = []
    all_data_fetched = False
    total_games_saved = 0
    
    try:
        response = requests.get(f'{BASE_URL}{endpoint}', params=params)
        response.raise_for_status()
        data = response.json()
        all_games_data.extend(data['results'])
        
        print("Fetching and saving data...")
        for game in data['results']:
            # Save game data with cleaned file name
            sanitized_name = sanitize_filename(game["name"])
            if sanitized_name:
                file_name = os.path.join(file_path, f'{sanitized_name}.json')
                with open(file_name, 'w') as f:
                    json.dump(game, f, indent=4)
                total_games_saved += 1
                print(f"Saved game: {game['name']} to {file_name}")
            else:
                print(f"Skipping game: {game['name']} because the filename is invalid.")
        
        while data['next']:
            try:
                response = requests.get(data['next'])
                response.raise_for_status()
                data = response.json()
                all_games_data.extend(data['results'])
                
                for game in data['results']:
                    sanitized_name = sanitize_filename(game["name"])
                    if sanitized_name:
                        file_name = os.path.join(file_path, f'{sanitized_name}.json')
                        with open(file_name, 'w') as f:
                            json.dump(game, f, indent=4)
                        total_games_saved += 1
                        print(f"Saved game: {game['name']} to {file_name}")
                    else:
                        print(f"Skipping game: {game['name']} because the filename is invalid.")
                    
                time.sleep(0.2)
            
            except requests.exceptions.RequestException as err:
                print(f"Encountered a request issue: {err}. Skipping to the next request.")
                continue
            
            except json.JSONDecodeError as err:
                print(f"JSON decode error: {err}. Skipping to the next request.")
                continue
            
    except requests.exceptions.RequestException as err:
        print(f"Encountered a request issue: {err}")
        all_data_fetched = True
    
    except json.JSONDecodeError as err:
        print(f"JSON decode error: {err}")
        all_data_fetched = True
    
    finally:
        print(f"Total games saved: {total_games_saved}")

# Call function
fetch_and_save_data(r"C:\Users\NeilLaptop\OneDrive\Data Science\ds-final-project-main\data")

#%% Round 2 Scraping

# Only save games that are not currently in the dataset

BASE_URL = 'https://api.rawg.io/api/'
endpoint = 'games'
params = {
    'page_size': 100,
    'ordering': '-ratings_count',
    'key': API_KEY,
    'page': 1
}

# Function to replace invalid characters
def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*,.)()]', '_', name)

def fetch_existing_game_names(csv_file):
    existing_game_names = set()
    with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            existing_game_names.add(row['name'])
    return existing_game_names

def fetch_and_save_data(file_path, csv_file):
    existing_game_names = fetch_existing_game_names(csv_file)
    total_games_saved = 0
    page_number = params['page']
    
    while True:
        try:
            response = requests.get(f'{BASE_URL}{endpoint}', params=params)
            response.raise_for_status()
            data = response.json()

            print(f"Fetching data from page {page_number}...")
            for game in data['results']:
                name = game["name"]
                if name not in existing_game_names:
                    sanitized_name = sanitize_filename(name)
                    if sanitized_name:
                        try:
                            file_name = os.path.join(file_path, f'{sanitized_name}.json')
                            with open(file_name, 'w') as f:
                                json.dump(game, f, indent=4)
                            total_games_saved += 1
                            print(f"Saved game: {name} to {file_name}")
                        except OSError as e:
                            if e.errno == 22:
                                print(f"Skipping game: {name} due to invalid argument error.")
                            else:
                                raise e
                    else:
                        print(f"Skipping game: {name} - filename is invalid.")
                else:
                    print(f"Skipping game: {name} - dupe.")

            while data['next']:
                try:
                    response = requests.get(data['next'])
                    response.raise_for_status()
                    data = response.json()

                    page_number += 1
                    print(f"Fetching data from page {page_number}...")
                    
                    for game in data['results']:
                        name = game["name"]
                        if name not in existing_game_names:
                            sanitized_name = sanitize_filename(name)
                            if sanitized_name:
                                try:
                                    file_name = os.path.join(file_path, f'{sanitized_name}.json')
                                    with open(file_name, 'w') as f:
                                        json.dump(game, f, indent=4)
                                    total_games_saved += 1
                                    print(f"Saved game: {name} to {file_name}")
                                except OSError as e:
                                    if e.errno == 22:
                                        print(f"Skipping game: {name} - invalid argument error.")
                                    else:
                                        raise e
                            else:
                                print(f"Skipping game: {name} - filename is invalid.")
                        else:
                            print(f"Skipping game: {name} - dupe.")

                    time.sleep(0.2)

                except requests.exceptions.RequestException as err:
                    print(f"Request issue: {err}. Retrying...")
                    continue

                except json.JSONDecodeError as err:
                    print(f"JSON decode error: {err}. Retrying...")
                    continue

            break

        except requests.exceptions.RequestException as err:
            print(f"Request issue: {err}. Retrying...")
            continue

        except json.JSONDecodeError as err:
            print(f"JSON decode error: {err}. Retrying...")
            continue

    print(f"Total games saved: {total_games_saved}")

# Call function
fetch_and_save_data(r"C:\Users\Niocu\OneDrive\Data Science\ds-final-project-main\data", 
                    r"C:\Users\Niocu\OneDrive\Data Science\ds-final-project-main\data\updated_data.csv")