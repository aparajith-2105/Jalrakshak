from datetime import date, timedelta
import requests

API = "https://power.larc.nasa.gov/api/temporal/daily/point"

def fetch_daily_weather(latitude: float, longitude: float):
    """Fetch latest complete daily mean temperature, RH, and precipitation from NASA POWER."""
    end = date.today() - timedelta(days=2)  # Recent daily values may be delayed.
    start = end - timedelta(days=6)
    params = {"parameters":"T2M,RH2M,PRECTOTCORR", "community":"AG", "longitude":longitude,
              "latitude":latitude, "start":start.strftime("%Y%m%d"), "end":end.strftime("%Y%m%d"), "format":"JSON"}
    try:
        response = requests.get(API, params=params, timeout=15)
        response.raise_for_status()
        values = response.json()["properties"]["parameter"]
        def latest_valid(series):
            valid = [(k, v) for k, v in series.items() if v is not None and float(v) > -900]
            return valid[-1] if valid else None
        temp = latest_valid(values["T2M"])
        humidity = latest_valid(values["RH2M"])
        rain = latest_valid(values["PRECTOTCORR"])
        if not all((temp, humidity, rain)):
            return None
        return {"temperature":float(temp[1]), "humidity":float(humidity[1]), "rainfall":max(0.0,float(rain[1])), "date":temp[0]}
    except (requests.RequestException, KeyError, ValueError, TypeError):
        return None
