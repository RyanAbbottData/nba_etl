from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd

app = FastAPI()
templates = Jinja2Templates(directory=".")

@app.get("/", response_class=HTMLResponse)
async def read_csv_table(request: Request):
    # Load CSV data
    player_df = pd.read_csv("../data/current_player_predictions.csv").head(25)
    team_df = pd.read_csv("../data/current_team_predictions.csv")

    # Renaming and Filtering columns
    player_df = player_df.rename(columns={"rank_logistic": "rank"})
    team_df = team_df.rename(columns={"output_linear": "projected_win_pct"})
    print(team_df.columns)
    print(player_df.columns)
    team_df['projected_wins'] = team_df['projected_win_pct'] * 82

    player_display_cols = ["PLAYER_NAME", "rank", "PTS/G", "REB/G", "AST/G", "TOV/G", "STL/G", "BLK/G", "GP_PCT", "W_PCT", "last_updated"]
    team_display_cols = ["Team", "projected_win_pct", "projected_wins", "playoff_chance", "mean_percentile", "best_player", "last_updated"]



    # Convert DataFrame to a list of dictionaries
    player_data_filtered = player_df[player_display_cols].to_dict(orient="records")
    team_data_filtered = team_df[team_display_cols].to_dict(orient="records")

    # Render the data in the HTML template
    return templates.TemplateResponse("table.html", {"request": request, "player_data": player_data_filtered, "team_data": team_data_filtered})

