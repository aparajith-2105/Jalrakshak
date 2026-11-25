# 🌱 Jalrakshak — Intelligent Irrigation Prediction System

Jalrakshak is a crop irrigation decision-support project. It uses field conditions, weather information, and a trained machine learning model to estimate whether irrigation need is **Low**, **Medium**, or **High**.

The goal is to help users make more informed irrigation decisions and reduce the risk of over-irrigation or under-irrigation. The system provides an estimate for review; it does not operate pumps or valves.

**Live-Dashboard:**https://jalrakshak-snce.onrender.com

## The problem

Irrigation decisions can be difficult when field readings are incomplete, inaccurate, or out of date. Soil sensors may drift, become fouled, or stop working. A system that relies on one reading without checking its quality may recommend too much or too little water.

Jalrakshak brings crop, soil, weather, and optional sensor-history information together in one dashboard. It is designed to show an irrigation estimate and highlight possible sensor concerns when the relevant readings are provided.

## Project objectives

- Estimate irrigation need from the available field and weather inputs.
- Present the result in a dashboard that is easy to understand.
- Use optional sensor readings or uploaded sensor history to support sensor-health checks.
- Show the datasets and model information used by the project.
- Keep the result as decision support so that users can verify field conditions before acting.

## Dashboard features

### Field dashboard

Users can enter details such as:

- Region, crop, growth stage, soil type, and season
- Field area
- Soil moisture, temperature, and relative humidity
- Recent rainfall, sunlight, and wind speed
- Soil pH, organic carbon, and electrical conductivity
- Previous irrigation, irrigation method, and water source
- Optional location coordinates for NASA POWER weather data

The dashboard uses the supplied values to produce an irrigation-need estimate and related guidance.

### Sensor health

Sensor-health inputs are optional. Users can provide readings from multiple probes or upload sensor-history data, where supported, to help identify readings that may be stale, inconsistent, or unusual.

This is a check on the data provided to the application. It does not mean that the project is automatically connected to physical IoT sensors or continuously monitoring a field.

### Model and data

This section presents information about the model, its evaluation, and the data files included with the project. Evaluation results describe performance on the available dataset; they do not guarantee the same performance in every field.

### Recommendation history

This section displays saved recommendations when history is available in the running application.

## Data used

The project uses the supplied datasets for different purposes. They are not all combined into one training table.

| Dataset | Project use |
|---|---|
| `irrigation_prediction.csv` | Main supervised dataset for predicting the `Irrigation_Need` label |
| `Crop_recommendation.csv` | Crop and agronomy reference data |
| `weather-1.csv` | Weather context and reference data |
| `IOT-temp.csv` | Temperature readings; these are not soil-moisture measurements |
| `plant_vase1.CSV`, `plant_vase1(2).CSV`, `plant_vase2.CSV` | Plant or moisture sensor logs for reference and optional sensor analysis |
| `csv` | Agricultural market-price reference data, where included |
| NASA POWER daily data | Weather information for a selected location and date range, when requested by the application |

The role of each dataset depends on its columns and quality. A dataset is not treated as a model input or an irrigation label unless its contents support that use.

## Model and methodology

1. The project loads and examines the available datasets.
2. The irrigation training data is prepared for supervised learning.
3. A classification model is trained to predict the irrigation-need category.
4. The model is evaluated using held-out data and classification metrics.
5. The dashboard passes user-provided field values to the trained model and displays its prediction.

The model predicts the categories represented in its training data. Entering values in the dashboard requests a prediction; it does **not** automatically add those values to the training data or retrain the model.

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

## Deploying the static dashboard on Render

Render Static Sites can serve the HTML, CSS, JavaScript, and other static files in this project.

1. Sign in to [Render](https://render.com/).
2. Select **New → Static Site**.
3. Connect GitHub and select the `Jalrakshak` repository.
4. Select the branch you want to deploy, usually `main`.
5. Leave **Build Command** blank for a plain static site.
6. Set **Publish Directory** to `.` if `index.html` is in the repository root.
7. Create the static site and wait for deployment to finish.


Render redeploys the connected site when changes are pushed to the selected Git branch. See the [Render Static Sites guide](https://render.com/docs/static-sites).

> **Important:** A Render Static Site serves static files. It does not run `app.py` or a Streamlit server. If the dashboard needs a Python backend to make predictions, that backend must be hosted separately and the frontend must be configured to connect to it.

## Limitations

- Predictions depend on the quality and coverage of the training data.
- Training labels may not represent verified water volumes or audited field outcomes.
- Sensor checks depend on the readings and history supplied to the application.
- NASA POWER data provides weather context; it does not replace local field measurements.
- Recommendations are estimates and should be checked against local conditions and agricultural guidance.
- The project is a prototype and should not directly control irrigation hardware without further testing.

## Future improvements

- Collect field data with verified irrigation outcomes.
- Validate the model across crops, regions, soil types, and seasons.
- Add more labeled examples of sensor drift, fouling, and hardware failure.
- Connect physical sensors through a secure IoT service.
- Compare recommendations with expert or field-validated decisions.

## References

- [NASA POWER API documentation](https://power.larc.nasa.gov/docs/services/api/temporal/daily/)
- [Render Static Sites documentation](https://render.com/docs/static-sites)

## Project note

Jalrakshak is an educational decision-support project. Always confirm field conditions before making irrigation decisions.