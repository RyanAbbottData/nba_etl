import os
import sys

import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier


# Determine the project root directory
project_root = os.path.abspath(os.path.join(os.getcwd(), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

from utils.models import save_model
from utils.formats import encode_column, get_win_pct_from_record
from utils.normalization import get_stats_normalized_by_year

df = pd.read_csv("../data/team_season_data.csv").query("season_end_year > 2000")
print(df[['TeamID', 'TeamCity', 'TeamName']])
stats = pd.read_csv("../data/player_season_data_prepared.csv")[['TEAM_ID', 'season_end_year', "GP_PCT",  "W_PCT", "FG_PCT", "FG3_PCT", "FT_PCT", "REB/G", "AST/G", "TOV/G", "STL/G", "BLK/G", "PLUS_MINUS", "DD2_rate", "TD3_rate", "PTS/G"]]
print(stats[["PLUS_MINUS", "DD2_rate", "TD3_rate"]])

PLAYER_COLUMN = 'PLAYER_NAME'
YEAR_COLUMN = 'season_end_year'
TEAM_COLUMN_PLAYERS = 'TEAM_ID'
TEAM_COLUMN_TEAMS = 'TeamID'

player_percentiles = get_stats_normalized_by_year(df=stats, columns_to_skip=[YEAR_COLUMN, TEAM_COLUMN_PLAYERS])

player_percentiles['mean_percentile'] = player_percentiles.drop(columns=[YEAR_COLUMN, TEAM_COLUMN_PLAYERS]).mean(axis=1, numeric_only=True, skipna=True)
team_mean_percentiles = player_percentiles.groupby([TEAM_COLUMN_PLAYERS, YEAR_COLUMN]).mean()
team_max_percentiles = player_percentiles.groupby([TEAM_COLUMN_PLAYERS, YEAR_COLUMN]).max()

print(team_max_percentiles.columns)
df = df.merge(team_mean_percentiles, left_on=[TEAM_COLUMN_TEAMS, YEAR_COLUMN], right_on=[TEAM_COLUMN_PLAYERS, YEAR_COLUMN])
df = df.merge(team_max_percentiles['mean_percentile'], left_on=[TEAM_COLUMN_TEAMS, YEAR_COLUMN], right_on=[TEAM_COLUMN_PLAYERS, YEAR_COLUMN])

df = df.rename(columns={'mean_percentile_y': "best_player",
                        'mean_percentile_x': "mean_percentile"})

print(df.columns)



df['WinPCT'] = df["WINS"] / (df["WINS"] + df['LOSSES'])

x_columns = ['Conference', 'ConferenceRecord', 'OT', 'ThreePTSOrLess', 'TenPTSOrMore',
       'AheadAtHalf', 'BehindAtHalf', 'TiedAtHalf', 'AheadAtThird',
       'BehindAtThird', 'TiedAtThird', 'Score100PTS', 'OppScore100PTS',
       'OppOver500', 'LeadInFGPCT', 'LeadInReb', 'FewerTurnovers', 'DiffPointsPG', 'mean_percentile', 'best_player']

y_column_1 = 'WinPCT'
y_column_2 = 'ClinchedPlayoffBirth'

x = df[x_columns]
x_playoffs = df[df['season_end_year'] != 2001][x_columns]
x_playoffs = encode_column(col="Conference", x=x_playoffs)
y_win_pct = df[y_column_1]
y_playoffs = df[y_column_2]

x = encode_column(col="Conference", x=x)

record_cols = ['ConferenceRecord', 'OT', 'ThreePTSOrLess', 'TenPTSOrMore',
       'AheadAtHalf', 'BehindAtHalf', 'TiedAtHalf', 'AheadAtThird',
       'BehindAtThird', 'TiedAtThird', 'Score100PTS', 'OppScore100PTS',
       'OppOver500', 'LeadInFGPCT', 'LeadInReb', 'FewerTurnovers']

x[record_cols] = x[record_cols].applymap(lambda z: get_win_pct_from_record(z))
x_playoffs[record_cols] = x_playoffs[record_cols].applymap(lambda z: get_win_pct_from_record(z))

x = x.fillna(-1)  # Remove rows with missing values if any
x_playoffs = x_playoffs.fillna(-1)
y_playoffs = y_playoffs.dropna()

y_win_pct = y_win_pct.iloc[x.index]

x_playoffs = x_playoffs.reset_index(drop=True)
y_playoffs = y_playoffs.reset_index(drop=True)
y_playoffs = y_playoffs.iloc[x_playoffs.index]


print(x.columns)
#model_log = LogisticRegression(max_iter=1000).fit(x,y)
model_lin_win_pct = LinearRegression().fit(x,y_win_pct)
model_rf_playoffs = RandomForestClassifier().fit(x_playoffs,y_playoffs)
#model_rand_for = RandomForestClassifier().fit(x,y)

path = "../models/"
#save_model(path + "team_model_log.pkl", model_log)
save_model(path + "team_model_lin_win_pct.pkl", model_lin_win_pct)
save_model(path + "team_model_rf_playoffs.pkl", model_rf_playoffs)
#save_model(path + "team_model_rand_for.pkl", model_rand_for)