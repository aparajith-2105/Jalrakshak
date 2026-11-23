# Jalrakshak — Intelligent Irrigation Prediction System

A standalone dashboard that uses a browser-side k-nearest-neighbors classifier on the included irrigation dataset, accepts field and crop inputs, and optionally retrieves recent NASA POWER daily weather. The `index.html` version is static and can be hosted by any static web host. It does not require a Python server or prediction API.

## Run or host the static dashboard

Keep `index.html` and the `data` folder together. Run a local static web server from this folder (for example, VS Code Live Server) and open the served page. Directly opening the HTML with a `file://` URL may prevent the browser from fetching the training CSV. To host, upload the folder contents to any static hosting provider; no provider-specific configuration is needed. NASA POWER lookup needs internet access and a browser that permits the NASA API request; manual weather inputs remain available if the request fails.

The project also retains an optional Streamlit/Python version (`app.py`) for local use. It is separate from the static dashboard.

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this folder and create an environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements-local.txt
   streamlit run app.py
   ```

The Streamlit model trains at startup using `data/irrigation_prediction.csv`. Recommendations are stored in `jalrakshak.sqlite3` in this folder. NASA POWER lookup needs an internet connection and latitude/longitude; if unavailable, the app uses the manual weather values entered by the user.

## What is included

- `data/irrigation_prediction.csv` — supervised training data with `Irrigation_Need` labels.
- `data/Crop_recommendation.csv` — agronomy reference dataset.
- `data/weather-1.csv` — state/district weather snapshot.
- `data/IOT-temp.csv` — indoor/outdoor temperature log.
- `data/plant_vase*.CSV` — plant moisture sensor logs.
- `data/csv` — agricultural market price data.
- `model.py` — preprocessing, stratified holdout evaluation, and classifier training.
- `database.py` — SQLite recommendation history.
- `nasa_power.py` — NASA POWER daily API integration.

## Data interpretation and limits

The classifier predicts the `Low`, `Medium`, or `High` label found in the supplied irrigation dataset. It does not calculate verified liters or valve runtime. The label's physical meaning and source quality have not been independently verified, and the classes are imbalanced. The dashboard displays held-out accuracy and macro F1 so users can see basic performance, but these scores do not establish farm-level validity.

`IOT-temp.csv` contains air temperature, not soil moisture. All irrigation labels in the three supplied plant vase files were `False`, so they cannot teach a positive/negative irrigation-action model. These auxiliary datasets are included for later exploration and are not silently mixed into training. `weather-1.csv` is a 2025 snapshot and is not treated as current live weather. The NASA links originally shared were duplicate documentation URLs; runtime data is requested from the NASA POWER API endpoint.

Treat predictions as decision support. Validate the model against local crop, soil, sensor, and irrigation outcomes before operational use. Sensor drift/fouling detection and calibrated water-volume recommendations need labeled field data and hardware details and are not claimed in this starter build.

## Database

SQLite stores each user-submitted recommendation, its input values, prediction, model probability, and weather source. The database file is created on first launch and is excluded from source control by `.gitignore`.
