# Jalrakshak — Intelligent Irrigation Prediction System

A dashboard that trains a Random Forest classifier on the included irrigation dataset, accepts field and crop inputs, and optionally retrieves recent NASA POWER daily weather. It includes both a Vercel-ready browser dashboard and a local Streamlit dashboard.

## Deploy on Vercel

1. Push the contents of this folder to a GitHub repository.
2. Import that repository in Vercel and deploy with the default static build settings (no build command or output directory is required).
3. `index.html` is the browser dashboard; `api/predict.py` is the Python prediction function. Vercel's Python runtime is currently Beta. The function trains/caches the model within each warm serverless instance, so the first prediction can take longer.
4. The Vercel version stores history in the browser's local storage on that device. Local SQLite history is only used by the Streamlit version.

The project root contains `requirements.txt` for the Python function. Keep the included `data/irrigation_prediction.csv`; the API needs it to train the model.

## Test the Vercel version locally before deploying

Do not use VS Code Live Server or open `index.html` directly for predictions: those only serve the page and do not run `/api/predict`. From this project folder, install the Vercel CLI and run its local development server:

```powershell
npm install --global vercel
vercel dev
```

Open the local URL printed by `vercel dev`. This runs the page and Python API together without deploying. The first prediction can take time while the classifier trains. Alternatively, run the separate Streamlit version with `streamlit run app.py` after installing `requirements-local.txt`.

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
