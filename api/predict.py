"""Vercel Python function serving the irrigation prediction endpoint."""
from http.server import BaseHTTPRequestHandler
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from model import load_training_data, train_model, FEATURES
from nasa_power import fetch_daily_weather

_bundle = None

def get_bundle():
    global _bundle
    if _bundle is None:
        data = load_training_data(ROOT / "data" / "irrigation_prediction.csv")
        model, metrics, data, target = train_model(data)
        _bundle = (model, metrics, data, target)
    return _bundle

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length))
            model, metrics, data, target = get_bundle()
            weather_source = "Manual inputs"
            if payload.get("use_nasa"):
                weather = fetch_daily_weather(float(payload.get("latitude", 20)), float(payload.get("longitude", 78)))
                if weather:
                    payload.update({"Temperature_C":weather["temperature"], "Humidity":weather["humidity"], "Rainfall_mm":weather["rainfall"]})
                    weather_source = "NASA POWER · " + weather["date"]
                else:
                    weather_source = "Manual inputs · NASA unavailable"
            row = {name: payload[name] for name in FEATURES}
            import pandas as pd
            X = pd.DataFrame([row], columns=FEATURES)
            prediction = str(model.predict(X)[0])
            probabilities = {str(c):float(p) for c,p in zip(model.classes_, model.predict_proba(X)[0])}
            body = {"prediction":prediction,"confidence":max(probabilities.values()),"probabilities":probabilities,"weather_source":weather_source,"metrics":{"accuracy":metrics["accuracy"],"macro_f1":metrics["macro_f1"],"rows":len(data)}}
            encoded = json.dumps(body).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)
        except Exception as exc:
            encoded = json.dumps({"error":str(exc)}).encode("utf-8")
            self.send_response(400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)
