# ------------------ Project Description ------------------
The concept for this project was to build a dashboard that can be used to identify trends in video game releases and ratings, in order to identify patterns and for use by game developers to determine what genres, platforms, stores, tags, release dates, etc. may be best to improve chances of a successful game release.

For example, a developer looking to release a Co-op Card game could enter those as a tag and genre respectively and see what other tags and genres are most often used in association with these, the average rating these combinations of tags and genres tend to receive, what platforms and stores these types of games are best received on, and all possible release dates that would avoid other big game releases.


# ------------------ Notebook Explanations ----------------
RAWG Scraper
- Calls RAWG API to fetch game data
- Sanitizes file names to avoid issues with saving files
- Skips games that cause errors in order to avoid interrupting code
-- Ex: invalid file names, JSON decode errors, request issues
- Saves each game's data as its own .json file
- "Round 2 Scraper" functions the same but ignores games already in a given
-- data base, used for repeat passes to catch missed/skipped games

Combine Data
- Combines json files from RAWG Scraper into one csv file
- Skips JSON decoding errors and tracks files processed

Data Exploration and Cleaning
- Used to get an overview of the data
- Removed unnecessary columns
- Cleaned up formatting of columns with multiple values
- Changed strings to dictionaries, removed "slug:" "name:" statements
- Created sample ratings plot to visualize data
- Identified all unique release years, platforms, genres, stores, tags, and Ratings
- -And their counts
- Added month and month/day columns
- Identified and removed duplicates
- Removed brackets from dictionaries for compatibility with Tableau
- Reset index to have consistent unique identifiers per game
- Averaged out player ratings and metacritic to get an average rating


# ------------------ Data Explanation ---------------------
*Final dataset is split into 5 csv files
**Master dataset and splits to seperate cells containing multiple values into multiple entries for ease of use **in Tableau filters

Data is taken from RAWG video game databased (unfiltered) with games from 10 different stores and 50 different platforms. Databased currently contains information from 410,107 different games.

engineered_dataset
- Index
- -Contains a unique identifier used to identify games and link different data files
- Slug
- -Contains the game's name formatted for use in APIs, to be potentially used in future data collection
- Name
- -Contains the game's title
- Released
- -Contains the game's release date formatted as YYYY-MM-DD
- Platforms
- -Contains the platforms the game is available on
- Genres
- -Contains all of the game's genres
- Stores
- -Contains the stores the game can be purchased on
- Tags
- Contains all tags associated with the game
- ESRB Rating
- -Contains the game's ESRB Rating
- Overall Rating
- -Contains the game's averaged out user score and metacritic rating

- split_tags
- -Contains all data from engineered_dataset with each game split into multiple entries (one for each tag)

- split_stores
- -Contains all data from engineered_dataset with each game split into multiple entries (one for each store)

- split_platforms
- -Contains all data from engineered_dataset with each game split into multiple entries (one for each platform)

- split_genres
- -Contains all data from engineered_dataset with each game split into multiple entries (one for each genre)


# ------------------ Dashboard Links -----------------------
https://public.tableau.com/app/profile/neil.aucoin/viz/VideoGameFeatureRatings/BestRatedFeatures?publish=yes

https://public.tableau.com/app/profile/neil.aucoin/viz/MostCommonVideoGameFeatures/MostCommonFeatures?publish=yes
