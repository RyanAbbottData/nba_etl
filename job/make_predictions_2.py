import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier

import sys
import os
from enum import Enum

# Determine the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

from utils.models import load_model


class DataType(Enum):
    TEAM = "team"
    PLAYER = "player"


def make_predictions(type):
    df_current = pd.read_csv(f"../data/{type}_season_data_current_prepared.csv", encoding='utf-8')

    if type == DataType.PLAYER.value:

        x_columns = ["GP_PCT",  "W_PCT", "FG_PCT", "FG3_PCT", "FT_PCT", "REB/G", "AST/G", "TOV/G", "STL/G", "BLK/G", "PLUS_MINUS", "DD2_rate", "TD3_rate", "PTS/G"]
        columns_to_drop = ["FG_PCT", "FG3_PCT", "FT_PCT", "PLUS_MINUS", "DD2_rate", "TD3_rate", ]
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

        df_current.drop(columns=columns_to_drop).sort_values(by='rank_logistic', ascending=True).reset_index(
            drop=True).to_csv(f"../data/current_{type}_predictions.csv", index=False)

    if type == DataType.TEAM.value:

        x_columns = ['ConferenceRecord', 'OT', 'ThreePTSOrLess', 'TenPTSOrMore',
       'AheadAtHalf', 'BehindAtHalf', 'TiedAtHalf', 'AheadAtThird',
       'BehindAtThird', 'TiedAtThird', 'Score100PTS', 'OppScore100PTS',
       'OppOver500', 'LeadInFGPCT', 'LeadInReb', 'FewerTurnovers',
       'DiffPointsPG', 'mean_percentile', 'best_player', 'Conference_East',
       'Conference_West']

        player_rankings = pd.read_csv(f"../data/current_player_predictions.csv")['rank_logistic']


        all_columns = ["Team"] + x_columns + ["last_updated"]

        model_lin = load_model("../models/team_model_lin_win_pct.pkl")
        model_playoffs = load_model("../models/team_model_rf_playoffs.pkl")

        df_current = df_current[all_columns]

        df_current['output_linear'] = model_lin.predict(df_current[x_columns])
        df_current['rank_linear'] = df_current['output_linear'].rank(ascending=False)
        playoff_chances = [chance[1] for chance in model_playoffs.predict_proba(df_current[x_columns])]
        df_current['playoff_chance'] = playoff_chances

        x_columns.remove("mean_percentile")
        x_columns.remove("best_player")
        df_current.drop(columns=x_columns).sort_values(by='rank_linear', ascending=True).reset_index(drop=True).to_csv(f"../data/current_{type}_predictions.csv", index=False)