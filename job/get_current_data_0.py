from nba_api.stats.endpoints import leaguedashplayerstats
import pandas as pd

import sys
import os

# Determine the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

from utils.formats import get_seasons_in_correct_format
from utils.previous_mvps import nba_mvp_list


def get_current_data():
    # grabbing data for this year
    years = get_seasons_in_correct_format(start_year = 2024, end_year = 2025)

    # Master df to collect season stats
    master_df = pd.DataFrame()

    # Getting the data for current season
    for season in years:

        player_stats = leaguedashplayerstats.LeagueDashPlayerStats(season=season)

        stats_df = player_stats.get_data_frames()[0]


        # I know this is bad practice
        # If I'm still doing this by 2100 then screw me
        stats_df["season_end_year"] = "20" + season[-2:]
        stats_df["season"] = season

        master_df = pd.concat([master_df, stats_df])

    # Removing aposthrophes from names, which are causing issues with quotation
    master_df['PLAYER_NAME'] = master_df['PLAYER_NAME'].replace("'", "")

    # Writing the CSV
    master_df.to_csv("../data/player_season_data_current.csv", index=False)