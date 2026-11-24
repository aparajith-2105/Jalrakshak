# Jalrakshak

Jalrakshak is an irrigation dashboard. It uses crop, soil, and weather information to estimate irrigation need as **Low**, **Medium**, or **High**.

# Demo: 
https://jalrakshak-d5zw.netlify.app/

## Two dashboard versions

- `app.py` runs the Streamlit version on your computer. It trains a Random Forest model from the irrigation dataset.
- `index.html` is the static website version. It uses a browser-based k-nearest-neighbors model and can be hosted on Vercel or another static web host.

The two versions work separately and use different prediction models.

## Run the Streamlit version in VS Code

Open the Jalrakshak folder in VS Code. Choose **Terminal → New Terminal**, then run these commands one at a time:

~~~powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-local.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
~~~

Open the local web address shown in the terminal.

## Run or host the static version

Keep `index.html` and the `data` folder together. To preview the dashboard, open the project with VS Code Live Server.

To host it, upload `index.html` and the `data` folder to Vercel or another static web host. The NASA POWER weather option needs an internet connection. If it is unavailable, enter weather values manually.

## **Database**

The Streamlit version saves recommendation history in a local SQLite database named `jalrakshak.sqlite3`. The app creates this file automatically.

Each saved recommendation includes the time, field inputs, prediction, confidence score, and weather source.

The static website saves history in the browser on that device. Browser history is not shared between users or devices.

## Sensor checks

The static dashboard can compare readings from multiple probes or check an uploaded sensor history CSV. History files should have moisture columns named like `moisture0`, `moisture1`, and so on.

The dashboard flags possible stale readings, unusual values, probes that disagree, repeated readings, and possible drift. These are warnings, not confirmation that a sensor has failed. The Streamlit version does not include these sensor checks.

## Data and limitations

The model uses `data/irrigation_prediction.csv`. Its labels are **Low**, **Medium**, and **High**; they are not exact water amounts or valve runtimes.

The other included CSV files are reference data. They are not all used to train the irrigation model. NASA POWER weather is optional and requires an internet connection and location coordinates.

Use the results as estimates and check field conditions before making irrigation decisions.
