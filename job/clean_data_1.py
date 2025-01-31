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
from utils.formats import encode_column, get_win_pct_from_record
from utils.normalization import get_stats_normalized_by_year

def clean_data(type):

    csv_name = f"../data/{type}_season_data_current"
    df = pd.read_csv(f"{csv_name}.csv")

    if type == "player":
        df['REB/G'] = df['REB'] / df['GP']
        df['AST/G'] = df['AST'] / df['GP']
        df['TOV/G'] = df['TOV'] / df['GP']
        df['STL/G'] = df['STL'] / df['GP']
        df['BLK/G'] = df['BLK'] / df['GP']
        df['PTS/G'] = df['PTS'] / df['GP']
        df['DD2_rate'] = df['DD2'] / df['GP']
        df['TD3_rate'] = df['TD3'] / df['GP']
        df['GP_PCT'] = df['GP'] / max(df['GP'])

        PLAYER_COLUMN = 'PLAYER_NAME'
        YEAR_COLUMN = 'season_end_year'
        TEAM_COLUMN = 'TEAM_ID'

        df = get_stats_normalized_by_year(df=df[['PLAYER_NAME', 'TEAM_ID', 'season_end_year', "GP_PCT",  "W_PCT", "FG_PCT", "FG3_PCT", "FT_PCT", "REB/G", "AST/G", "TOV/G", "STL/G", "BLK/G", "PLUS_MINUS", "DD2_rate", "TD3_rate", "PTS/G"]], columns_to_skip=[PLAYER_COLUMN, YEAR_COLUMN, TEAM_COLUMN])
    elif type == "team":
        PLAYER_COLUMN = 'PLAYER_NAME'
        YEAR_COLUMN = 'season_end_year'
        TEAM_COLUMN_PLAYERS = 'TEAM_ID'
        TEAM_COLUMN_TEAMS = 'TeamID'

        stats = pd.read_csv("../data/player_season_data_current_prepared.csv")[
            ['TEAM_ID', 'season_end_year', "GP_PCT", "W_PCT", "FG_PCT", "FG3_PCT", "FT_PCT", "REB/G", "AST/G", "TOV/G",
             "STL/G", "BLK/G", "PLUS_MINUS", "DD2_rate", "TD3_rate", "PTS/G"]]


        # Getting mean_percentile
        player_percentiles = get_stats_normalized_by_year(df=stats,columns_to_skip=[PLAYER_COLUMN, YEAR_COLUMN, TEAM_COLUMN_PLAYERS])

        player_percentiles['mean_percentile'] = player_percentiles.drop(
            columns=[YEAR_COLUMN, TEAM_COLUMN_PLAYERS]).mean(axis=1, numeric_only=True, skipna=True)
        team_mean_percentiles = player_percentiles.groupby([TEAM_COLUMN_PLAYERS, YEAR_COLUMN]).mean()
        team_max_percentiles = player_percentiles.groupby([TEAM_COLUMN_PLAYERS, YEAR_COLUMN]).max()
        team_mean_percentiles = team_mean_percentiles.reset_index(drop=False)
        team_max_percentiles = team_max_percentiles.reset_index(drop=False)

        print(df.columns)
        df = df.merge(team_mean_percentiles, left_on=[TEAM_COLUMN_TEAMS, YEAR_COLUMN],
                      right_on=[TEAM_COLUMN_PLAYERS, YEAR_COLUMN])
        print(team_max_percentiles.columns)
        df = df.merge(team_max_percentiles[['mean_percentile', TEAM_COLUMN_PLAYERS, YEAR_COLUMN]], left_on=[TEAM_COLUMN_TEAMS, YEAR_COLUMN],
                      right_on=[TEAM_COLUMN_PLAYERS, YEAR_COLUMN])

        df = df.rename(columns={'mean_percentile_y': "best_player",
                                'mean_percentile_x': "mean_percentile"})

        # Getting Win Percentage
        df['WinPCT'] = df["WINS"] / (df["WINS"] + df['LOSSES'])
        # Getting Player's Team
        df['Team'] = df['TeamCity'] + " " + df['TeamName']

        # Encoding Conferences
        df = encode_column(col="Conference", x=df)

        # Converting W-L records to Win Percentage
        record_cols = ['ConferenceRecord', 'HOME', 'ROAD', 'OT', 'ThreePTSOrLess', 'TenPTSOrMore',
                       'AheadAtHalf', 'BehindAtHalf', 'TiedAtHalf', 'AheadAtThird',
                       'BehindAtThird', 'TiedAtThird', 'Score100PTS', 'OppScore100PTS',
                       'OppOver500', 'LeadInFGPCT', 'LeadInReb', 'FewerTurnovers']
        df[record_cols] = df[record_cols].applymap(lambda z: get_win_pct_from_record(z))

        # Getting features
        x_columns = ["Team", 'ConferenceRecord', 'HOME', 'ROAD', 'OT', 'ThreePTSOrLess', 'TenPTSOrMore',
       'AheadAtHalf', 'BehindAtHalf', 'TiedAtHalf', 'AheadAtThird',
       'BehindAtThird', 'TiedAtThird', 'Score100PTS', 'OppScore100PTS',
       'OppOver500', 'LeadInFGPCT', 'LeadInReb', 'FewerTurnovers',
       'DiffPointsPG', 'Conference_East', 'Conference_West', 'mean_percentile', 'best_player']

        # Remove rows with missing values if any
        df = df[x_columns].fillna(-1)

    df['last_updated'] = datetime.today()

    df.to_csv(f"{csv_name}_prepared.csv", index=False)
