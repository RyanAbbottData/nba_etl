import pandas as pd

def get_seasons_in_correct_format(start_year: int = 2000,
                                  end_year: int = 2024,
                                  format: str = "YYYY-YY"):
    years = []
    num_years = end_year - start_year

    if num_years < 0:
        raise ValueError("Your end_year is earlier than your start year.")

    if format == "YYYY-YY":
        current_year = start_year
        for _ in range(num_years):
            year_after = current_year + 1
            formatted_season = str(current_year) + "-" + str(year_after)[-2:]
            years.append(formatted_season)

            current_year += 1

    return years


def get_win_pct_from_record(record: str):
    record_split = record.split("-")

    wins = int(record_split[0])
    losses = int(record_split[1])

    total_games = wins + losses

    try:
        win_pct = wins / total_games
    except ZeroDivisionError:
        win_pct = None

    return win_pct


def encode_column(col, x):
    dummy_cols = pd.get_dummies(x, columns=[col])

    for dummy_col in dummy_cols.columns:
        dummy_cols[dummy_col] = dummy_cols[dummy_col].replace(True, 1).replace(False, 0)

    return dummy_cols

