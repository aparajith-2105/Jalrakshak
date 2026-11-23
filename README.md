# Jalrakshak

Jalrakshak is an irrigation dashboard. It uses crop, soil, and weather details to estimate whether irrigation need is Low, Medium, or High.

## Two ways to use the dashboard

- `app.py` runs the Streamlit version on your computer.
- `index.html` is the static website version. Keep the `data` folder beside it. You can preview it with VS Code Live Server or host it on Vercel.

These versions work separately.

## Run the Streamlit version in VS Code

Open the Jalrakshak folder in VS Code. Open **Terminal → New Terminal**, then run:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-local.txt
.\.venv\Scripts\python.exe -m streamlit run app.py

## Database

The Streamlit version saves recommendation history in a local SQLite database named `jalrakshak.sqlite3`. It is created automatically when the app runs.

The static website version saves history in the browser on the same device. That history is not shared between users or devices.
