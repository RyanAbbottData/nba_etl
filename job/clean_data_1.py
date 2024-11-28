'''
Script to clean and prepare data
'''
import sys
import os

from datetime import datetime

import pandas as pd

# Determine the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

from utils.previous_mvps import nba_mvp_list


def clean_data():
    csv_name = "../data/player_season_data_current"
    df = pd.read_csv(f"{csv_name}.csv")

    df['REB/G'] = df['REB'] / df['GP']
    df['AST/G'] = df['AST'] / df['GP']
    df['TOV/G'] = df['TOV'] / df['GP']
    df['STL/G'] = df['STL'] / df['GP']
    df['BLK/G'] = df['BLK'] / df['GP']
    df['PTS/G'] = df['PTS'] / df['GP']
    df['DD2_rate'] = df['DD2'] / df['GP']
    df['TD3_rate'] = df['TD3'] / df['GP']
    df['GP_PCT'] = df['GP'] / max(df['GP'])

    df['last_updated'] = datetime.today()

    df.to_csv(f"../data/{csv_name}_prepared.csv", index=False)
