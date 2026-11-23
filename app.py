from __future__ import annotations

from pathlib import Path
import pandas as pd
import streamlit as st

from database import init_db, save_recommendation, recent_recommendations
from model import load_training_data, train_model, FEATURES, CATEGORICAL, NUMERIC
from nasa_power import fetch_daily_weather

ROOT = Path(__file__).parent
DATA = ROOT / "data"
st.set_page_config(page_title="Jalrakshak | Smart Irrigation", page_icon="💧", layout="wide")

st.markdown("""<style>
.stApp {background:linear-gradient(150deg,#f3f8f5 0%,#f7fafc 60%,#edf6f4 100%)}
[data-testid="stMetric"] {background:white;border:1px solid #e2ebe7;padding:16px;border-radius:14px}
.hero {padding:1.4rem 1.7rem;border-radius:20px;background:linear-gradient(110deg,#063f39,#087f70);color:white;margin-bottom:1rem}
.hero p {color:#d6f1e8;margin-bottom:0}
</style>""", unsafe_allow_html=True)

@st.cache_resource
def get_model():
    frame = load_training_data(DATA / "irrigation_prediction.csv")
    return train_model(frame)

init_db(ROOT / "jalrakshak.sqlite3")
try:
    model, metrics, frame, target_name = get_model()
except Exception as exc:
    st.error(f"Could not prepare the training data: {exc}")
    st.stop()

st.markdown('<div class="hero"><h1>💧 Jalrakshak</h1><p>Field-aware irrigation guidance with trained predictions, NASA weather context, and sensor checks.</p></div>', unsafe_allow_html=True)
page = st.sidebar.radio("Workspace", ["Irrigation dashboard", "Model & data", "Recommendation history"])
st.sidebar.caption("Decision support only. Confirm field conditions before operating pumps or valves.")

if page == "Irrigation dashboard":
    st.subheader("Tell us about the field")
    st.caption("The trained model estimates the irrigation-need class from the dataset's labeled examples. NASA POWER can supply recent weather when coordinates are available.")
    with st.form("field_inputs"):
        a,b,c = st.columns(3)
        states = sorted(frame["Region"].dropna().astype(str).unique())
        crops = sorted(frame["Crop_Type"].dropna().astype(str).unique())
        soils = sorted(frame["Soil_Type"].dropna().astype(str).unique())
        regions = a.selectbox("Region (training data)", states, index=None, placeholder="Select a region")
        crop = b.selectbox("Crop type", crops, index=None, placeholder="Select a crop")
        soil = c.selectbox("Soil type", soils, index=None, placeholder="Select soil type")
        d,e,f = st.columns(3)
        stage = d.selectbox("Growth stage", sorted(frame["Crop_Growth_Stage"].dropna().astype(str).unique()), index=None, placeholder="Select a stage")
        season = e.selectbox("Season", sorted(frame["Season"].dropna().astype(str).unique()), index=None, placeholder="Select a season")
        irr_type = f.selectbox("Irrigation method", sorted(frame["Irrigation_Type"].dropna().astype(str).unique()), index=None, placeholder="Select a method")
        g,h,i = st.columns(3)
        water_source = g.selectbox("Water source", sorted(frame["Water_Source"].dropna().astype(str).unique()), index=None, placeholder="Select a source")
        mulching = h.selectbox("Mulching used", ["Yes", "No"], index=None, placeholder="Select yes or no")
        area = i.number_input("Field area (hectares)", min_value=0.01, max_value=10000.0, value=1.0, step=0.1)
        j,k,l = st.columns(3)
        moisture = j.slider("Soil moisture (%)", 0.0, 100.0, float(frame.Soil_Moisture.median()))
        temperature = k.slider("Temperature (°C)", -5.0, 55.0, float(frame.Temperature_C.median()))
        humidity = l.slider("Relative humidity (%)", 0.0, 100.0, float(frame.Humidity.median()))
        m,n,o = st.columns(3)
        rainfall = m.number_input("Recent rainfall (mm)", min_value=0.0, max_value=2000.0, value=float(frame.Rainfall_mm.median()))
        previous = n.number_input("Previous irrigation (mm)", min_value=0.0, max_value=500.0, value=float(frame.Previous_Irrigation_mm.median()))
        sunlight = o.slider("Sunlight hours/day", 0.0, 24.0, float(frame.Sunlight_Hours.median()))
        p,q,r = st.columns(3)
        ph = p.slider("Soil pH", 3.0, 10.0, float(frame.Soil_pH.median()))
        organic = q.number_input("Organic carbon (%)", min_value=0.0, max_value=20.0, value=float(frame.Organic_Carbon.median()))
        ec = r.number_input("Electrical conductivity (dS/m)", min_value=0.0, max_value=100.0, value=float(frame.Electrical_Conductivity.median()))
        s,t = st.columns(2)
        wind = s.number_input("Wind speed (km/h)", min_value=0.0, max_value=300.0, value=float(frame.Wind_Speed_kmh.median()))
        latitude = t.number_input("Latitude for NASA POWER (optional)", min_value=-90.0, max_value=90.0, value=20.0, step=0.1)
        u,v = st.columns(2)
        longitude = u.number_input("Longitude for NASA POWER (optional)", min_value=-180.0, max_value=180.0, value=78.0, step=0.1)
        use_nasa = v.checkbox("Use latest NASA POWER daily weather", value=False)
        submitted = st.form_submit_button("Predict irrigation need", type="primary", use_container_width=True)

    if submitted:
        categorical_inputs = {"Region": regions, "Crop type": crop, "Soil type": soil, "Growth stage": stage,
                              "Season": season, "Irrigation method": irr_type, "Water source": water_source,
                              "Mulching used": mulching}
        missing = [label for label, value in categorical_inputs.items() if value is None]
        if missing:
            st.error("Please select: " + ", ".join(missing) + ".")
            st.stop()
        weather_note = "Manual weather inputs"
        if use_nasa:
            weather = fetch_daily_weather(latitude, longitude)
            if weather:
                temperature = weather.get("temperature", temperature)
                humidity = weather.get("humidity", humidity)
                rainfall = weather.get("rainfall", rainfall)
                weather_note = f"NASA POWER daily data ({weather.get('date','recent')})"
                st.info(f"Weather inputs updated from NASA POWER: {weather_note}. Check coordinates and data availability for your field.")
            else:
                st.warning("NASA POWER data could not be fetched; prediction uses the manual weather values above.")
        row = {
            "Soil_Type": soil, "Soil_pH": ph, "Soil_Moisture": moisture, "Organic_Carbon": organic,
            "Electrical_Conductivity": ec, "Temperature_C": temperature, "Humidity": humidity,
            "Rainfall_mm": rainfall, "Sunlight_Hours": sunlight, "Wind_Speed_kmh": wind,
            "Crop_Type": crop, "Crop_Growth_Stage": stage, "Season": season, "Irrigation_Type": irr_type,
            "Water_Source": water_source, "Field_Area_hectare": area, "Mulching_Used": mulching,
            "Previous_Irrigation_mm": previous, "Region": regions,
        }
        X = pd.DataFrame([row], columns=FEATURES)
        predicted = str(model.predict(X)[0])
        probs = model.predict_proba(X)[0]
        confidence = float(max(probs))
        classes = list(model.classes_)
        prob_map = dict(zip(classes, probs))
        st.divider()
        st.subheader("Recommendation")
        x,y,z = st.columns(3)
        x.metric("Predicted irrigation need", predicted)
        y.metric("Model confidence", f"{confidence:.0%}")
        z.metric("Weather source", "NASA POWER" if weather_note.startswith("NASA") else "Manual inputs")
        st.progress(confidence, text="Prediction confidence (model class probability)")
        st.write("**Why:** The model weighs crop and growth stage together with moisture, weather, soil properties, prior irrigation, and field context. Confidence is the classifier's probability, not a guarantee of field accuracy.")
        with st.expander("Class probability details"):
            st.bar_chart(pd.Series(prob_map, name="Model probability").sort_values(ascending=False))
        st.caption("The supplied training dataset has a strong class imbalance. Review the Model & data page before relying on results; recommendations are not automatic valve commands or calibrated water quantities.")
        sid = save_recommendation(ROOT / "jalrakshak.sqlite3", row, predicted, confidence, weather_note)
        st.success(f"Saved recommendation to local history (record {sid}).")

elif page == "Model & data":
    st.subheader("Training snapshot")
    st.write(f"Training target: **{target_name}**. The model is trained from `irrigation_prediction.csv` when the dashboard starts.")
    a,b,c = st.columns(3)
    a.metric("Training rows", f"{len(frame):,}")
    b.metric("Held-out accuracy", f"{metrics['accuracy']:.1%}")
    c.metric("Macro F1", f"{metrics['macro_f1']:.1%}")
    st.write("**Held-out classification report**")
    st.dataframe(pd.DataFrame(metrics["report"]).T.style.format(precision=2), use_container_width=True)
    st.write("**Training labels**")
    st.bar_chart(frame[target_name].value_counts())
    st.warning("The source dataset labels are Low/Medium/High. They are not verified liters, valve runtimes, or independently audited outcomes. Class imbalance and unknown dataset collection details limit real-world confidence. Validate locally before operational use.")
    st.subheader("Included data files")
    st.dataframe(pd.DataFrame([
        ["irrigation_prediction.csv", "Main supervised training data; target Irrigation_Need."],
        ["Crop_recommendation.csv", "Crop and agronomy reference; not merged into irrigation labels."],
        ["weather-1.csv", "State/district weather snapshot (2025); historical/contextual only."],
        ["IOT-temp.csv", "Indoor/outdoor air temperature log; not soil moisture."],
        ["plant_vase*.CSV", "Plant moisture sensor logs; all supplied irrigation labels are False."],
        ["csv", "Agricultural market prices; contextual reference, not model input."],
    ], columns=["File", "Use"]), hide_index=True, use_container_width=True)

else:
    st.subheader("Saved recommendations")
    history = recent_recommendations(ROOT / "jalrakshak.sqlite3")
    if history.empty:
        st.info("No recommendations saved yet. Make a prediction on the dashboard first.")
    else:
        st.dataframe(history, use_container_width=True, hide_index=True)
