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

from utils.models import load_model


def make_predictions():
    df_current = pd.read_csv("../data/player_season_data_current_prepared.csv", encoding='utf-8')

    x_columns = ["GP", "GP_PCT",  "W_PCT", "FG_PCT", "FG3_PCT", "FT_PCT", "REB/G", "AST/G", "TOV/G", "STL/G", "BLK/G", "PLUS_MINUS", "DD2_rate", "TD3_rate", "PTS/G"]

    all_columns = ["PLAYER_NAME"] + x_columns + ["last_updated"]

    model_log = load_model("../models/model_log.pkl")
    model_lin = load_model("../models/model_lin.pkl")
    model_rand_for = load_model("../models/model_rand_for.pkl")

    df_current = df_current[all_columns]

    df_current['output_logistic'] = [prob[1] for prob in model_log.predict_proba(df_current[x_columns])]
    df_current['output_linear'] = model_lin.predict(df_current[x_columns])
    df_current['output_rand_for'] = [prob[1] for prob in model_rand_for.predict_proba(df_current[x_columns])]

    df_current['rank_logistic'] = df_current['output_logistic'].rank(ascending=False)
    df_current['rank_linear'] = df_current['output_linear'].rank(ascending=False)
    df_current['rank_rand_for'] = df_current['output_rand_for'].rank(ascending=False)

    df_current['avg_rank'] = (df_current['rank_logistic'] + df_current['rank_linear'] + df_current['rank_rand_for']) / 3

    df_current.drop(columns=x_columns).sort_values(by='rank_logistic', ascending=True).reset_index(drop=True).to_csv("../data/current_predictions.csv")