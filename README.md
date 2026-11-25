# 🌱 Jalrakshak — Intelligent Irrigation Prediction System

Jalrakshak is a crop irrigation decision-support project. It uses field conditions, weather information, and a trained machine learning model to estimate whether irrigation need is **Low**, **Medium**, or **High**.

The goal is to help users make more informed irrigation decisions and reduce the risk of over-irrigation or under-irrigation. The system provides an estimate for review; it does not operate pumps or valves.

**Demo:** https://jalrakshak-d5zw.netlify.app/

## 🎯 What It Does

- Predicts irrigation need as **Low**, **Medium**, or **High**.
- Uses information such as crop type, soil moisture, temperature, rainfall, and humidity.
- Can request recent weather data from NASA POWER.
- Checks optional sensor readings for stale, unusual, or disagreeing values.
- Includes a simulation that shows how sensor drift can affect a prediction.
- Saves a history of recommendations.

## 🚀 Run the Dashboard in VS Code

1. Open the Jalrakshak project folder in VS Code.
2. Make sure `index.html` and the `data` folder are together in the same folder.
3. Install the **Live Server** extension if needed.
4. Right-click `index.html` and select **Open with Live Server**.

Use Live Server to open the dashboard. Opening the file directly with a `file://` address can prevent it from loading its training data.

## 🌐 Netlify Deployment

The static dashboard can be deployed through Netlify.

Make sure the published folder contains both `index.html` and the `data` folder. The data folder is needed for the dashboard to load its training examples.

The Netlify deployment hosts the static dashboard. The optional Streamlit app is a separate Python application.

## 🧪 Run the Optional Streamlit App

Open a PowerShell terminal in the project folder and run:

    py -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install -r requirements-local.txt
    streamlit run app.py

## 🧠 Model and Results

The browser dashboard loads `data/irrigation_prediction.csv` and uses a k-nearest-neighbors model to predict an irrigation need category.

The result is decision support. It is **not** a measured water quantity or valve runtime. The confidence shown is a model score and does not guarantee that the recommendation is correct for a particular field.

## Sensor limitations

The project is designed to support sensor-aware decision-making, but its checks depend on the readings and history supplied by the user. A reading that looks unusual should be checked against the field and, if possible, another probe.

The current project should not be described as automatically diagnosing every sensor fault. Reliable detection of drift, fouling, or hardware failure in real fields requires suitable sensor-history data and validation against known fault examples.

## Running locally

### Static dashboard

If you are using the static dashboard:

1. Download or clone this repository.
2. Open the project folder.
3. Open `index.html` in a browser, or serve the folder using VS Code Live Server.

Some browser features may require a local server instead of opening the HTML file directly.

### Python application

If you are using the Python or Streamlit application, install its dependencies and run it using the instructions for that application. A static HTML host does not run Python or Streamlit code.

## 🗂️ Included Data

The `data` folder contains:

- `irrigation_prediction.csv` — labeled examples used by the browser model.
- `Crop_recommendation.csv` — crop recommendation dataset.
- `weather-1.csv` — weather data snapshot.
- `IOT-temp.csv` — temperature readings.
- `plant_vase1.CSV`, `plant_vase1(2).CSV`, and `plant_vase2.CSV` — plant sensor readings.
- `csv` — additional agricultural data.

The dashboard does not automatically use every file for training. The browser model uses `irrigation_prediction.csv`.

## 🗄️ Database and Saved History

The CSV files in `data` are datasets. The optional Streamlit app uses SQLite to save recommendation records in `jalrakshak.sqlite3`.

The static browser dashboard stores recommendation history in the browser on the device where it is used.

## 🌦️ NASA POWER

Recent NASA POWER daily weather is optional and requires an internet connection and field coordinates. If the request is unavailable, users can enter weather values manually.

[NASA POWER daily API documentation](https://power.larc.nasa.gov/docs/services/api/temporal/daily/)

## ⚠️ Project Limitations

- Predictions are categories, not verified water amounts.
- Sensor warnings are rule-based checks; they do not prove that a sensor has failed.
- The simulation uses artificial readings and does not establish real-world sensor performance.
- Validate results with local crops, soil, sensors, and field measurements before using them for irrigation decisions.
