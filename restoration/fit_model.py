import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier

import sys
import os

# Determine the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

from utils.previous_mvps import nba_mvp_list
from utils.models import save_model

df_fit = pd.read_csv("../data/player_season_data_prepared.csv", encoding='utf-8')

mvp_indices = []
for mvp in nba_mvp_list:
    year = mvp['year']
    player = mvp['player']
    query = f"season_end_year == {year} and PLAYER_NAME == '{player}'"
    mvp_index = df_fit.query(query).index
    mvp_indices.append(mvp_index)

df_fit['is_mvp'] = 0
df_fit['is_mvp'].iloc[mvp_indices] = 1

x_columns = ["GP", "GP_PCT",  "W_PCT", "FG_PCT", "FG3_PCT", "FT_PCT", "REB/G", "AST/G", "TOV/G", "STL/G", "BLK/G", "PLUS_MINUS", "DD2_rate", "TD3_rate", "PTS/G"]
y_column = "is_mvp"

x = df_fit[x_columns]
y = df_fit[y_column]

model_log = LogisticRegression(max_iter=1000).fit(x,y)
model_lin = LinearRegression().fit(x,y)
model_rand_for = RandomForestClassifier().fit(x,y)

path = "../models/"
save_model(path + "model_log.pkl", model_log)
save_model(path + "model_lin.pkl", model_lin)
save_model(path + "model_rand_for.pkl", model_rand_for)




