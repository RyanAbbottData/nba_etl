import pandas as pd


def get_stats_normalized_by_year(df,
                                 columns_to_skip,
                                 keep_all_columns=True):
    '''
    A function to normalize statistics by year
    '''

    player_percentiles = pd.DataFrame()

    for col in df:
        if col not in columns_to_skip:
            player_percentiles[col] = df[col] / df.groupby('season_end_year').transform('max')[col]
        elif keep_all_columns:
            player_percentiles[col] = df[col]
        else:
            pass

    return player_percentiles