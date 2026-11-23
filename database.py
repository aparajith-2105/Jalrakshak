import json
import sqlite3
from pathlib import Path
import pandas as pd

def init_db(path: Path):
    with sqlite3.connect(path) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS recommendations (
          id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT NOT NULL DEFAULT (datetime('now','localtime')),
          inputs_json TEXT NOT NULL, predicted_need TEXT NOT NULL, confidence REAL NOT NULL, weather_source TEXT NOT NULL
        )""")

def save_recommendation(path: Path, inputs: dict, predicted: str, confidence: float, weather_source: str) -> int:
    with sqlite3.connect(path) as con:
        cur = con.execute("INSERT INTO recommendations(inputs_json,predicted_need,confidence,weather_source) VALUES(?,?,?,?)", (json.dumps(inputs), predicted, confidence, weather_source))
        return int(cur.lastrowid)

def recent_recommendations(path: Path, limit: int = 100) -> pd.DataFrame:
    with sqlite3.connect(path) as con:
        rows = con.execute("SELECT id,created_at,inputs_json,predicted_need,confidence,weather_source FROM recommendations ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    items=[]
    for ident, created, raw, need, confidence, source in rows:
        inp=json.loads(raw)
        items.append({"ID":ident,"Created":created,"Region":inp.get("Region"),"Crop":inp.get("Crop_Type"),"Need":need,"Confidence":f"{confidence:.0%}","Weather":source,"Soil moisture (%)":inp.get("Soil_Moisture")})
    return pd.DataFrame(items)
