"""
List of active players in the NBA
"""

# Import packages
import pandas as pd
import numpy as np
import html5lib
import string

# Load the data
player_df = pd.read_csv('/Users/alexcheng/Desktop/fastbreak_data/Workspace/Data/players.csv')

# Drop duplicates
player_df = player_df.drop_duplicates()

# Reset index
player_df = player_df.reset_index(drop=True)

# Change to list
player_list = list(player_df.values.flatten())

# Lowercase names, remove punctuation
player_list = [player.translate(None, string.punctuation).lower() for player in player_list]

# Create new columns
first_name = []
last_name = []
last_letter = []
player_id = []
first_two_first_name = []
player_num = []

for name in player_list:
    temp = []
    temp = name.split()
    first_name.append(temp[0])
    last_name.append(temp[1])
    last_letter.append(temp[1][0])
    player_id.append(temp[1][:5])
    first_two_first_name.append(temp[0][:2])
    player_num.append("01")

player_df['first_name'] = first_name
player_df['last_name'] = last_name
player_df['last_letter'] = last_letter
player_df['player_id'] = player_id
player_df['first_two_first_name'] = first_two_first_name
player_df['player_num'] = player_num

# Create 'player_id' column
player_df['player_id'] = player_df['player_id'] + player_df['first_two_first_name'] + player_df['player_num']

# Clean up the columns
player_df = player_df.drop(['first_name', 'last_name', 'first_two_first_name', 'player_num'], axis=1)

for i in player_df:
    player_df['url'] = "http://www.basketball-reference.com/players/%s/%s.html" % (player_df['last_letter'], player_df['player_id'])
