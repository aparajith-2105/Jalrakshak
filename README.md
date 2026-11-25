# 🌱 Jalrakshak — Smart Irrigation

Jalrakshak is an irrigation decision-support dashboard. It uses field and weather information to help estimate irrigation needs and display the results.

**Demo:** https://jalrakshak-snce.onrender.com

## Features

- Enter crop, soil, location, and weather details
- View an irrigation estimate and related guidance
- Explore the model and project data
- Review saved recommendation history

## Project files

- `index.html` — dashboard page
- `data/` or `Datasets/` — project data files
- `README.md` — project information

## Run the dashboard locally

1. Download or clone this repository.
2. Open the project folder.
3. Open `index.html` in a browser.

If the dashboard uses browser requests or local data files, run it with a local development server such as VS Code Live Server.

## Deploy on Render

This project can be deployed as a **Render Static Site** when the dashboard files are static HTML, CSS, and JavaScript.

1. Sign in to [Render](https://render.com/).
2. Select **New → Static Site**.
3. Connect GitHub and choose the `Jalrakshak` repository.
4. Select the branch to deploy, usually `main`.
5. Set **Build Command** to blank.
6. Set **Publish Directory** to `.` if `index.html` is in the repository's main folder.
7. Select **Create Static Site** and wait for the deployment to finish.

Render will show the website URL on the static site's page. Open that URL to view the dashboard and share it with others. When you push later changes to the connected branch, Render can deploy the updated files. See [Render's Static Site guide](https://render.com/docs/static-sites).

## Important

A Render **Static Site** serves files such as `index.html`. It does not run Python files such as `app.py` or a Streamlit application. If the dashboard depends on a Python backend, that backend must be deployed separately and the dashboard must be configured to connect to it.

## Data and model note

The dashboard provides estimates for decision support. Results depend on the available data and the values entered. Check field conditions before making irrigation decisions.

## Hosting

- **Host:** Render Static Sites
- **Website link:** https://jalrakshak-snce.onrender.com
