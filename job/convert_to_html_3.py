from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd

app = FastAPI()
templates = Jinja2Templates(directory=".")

@app.get("/", response_class=HTMLResponse)
async def read_csv_table(request: Request):
    # Load CSV data
    df = pd.read_csv("../data/current_predictions.csv")

    # Convert DataFrame to a list of dictionaries
    data = df.to_dict(orient="records")

    # Render the data in the HTML template
    return templates.TemplateResponse("table.html", {"request": request, "data": data})

