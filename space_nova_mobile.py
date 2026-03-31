import streamlit as st
import pandas as pd
import numpy as np
from skyfield.api import load, wgs84
import plotly.express as px

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Space Nova Protocol: Phase 9",
    layout="wide"
)

# -------------------------------
# Load Satellite Data
# -------------------------------
@st.cache_resource
def get_satellites():
    # Using 'visual' for faster loading during your launch
    url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=visual&FORMAT=tle"
    try:
        sats = load.tle_file(url, reload=True)
        return sats
    except:
        return None

# -------------------------------
# Collision Probability Model
# -------------------------------
def collision_probability(dist_km):
    sigma = 2.0  # uncertainty factor
    return np.exp(-(dist_km**2) / (2 * sigma**2))

# -------------------------------
# UI Header
# -------------------------------
st.title("🛰️ Space Nova: Autonomous Orbital Intelligence (Phase 9)")
st.markdown("### Decision-Grade Conjunction Analysis | TCA | Collision Risk")

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.header("System Status: OPERATIONAL")
st.sidebar.success("Mode: Advanced Conjunction Analysis Active")
st.sidebar.warning("Scanning future orbital paths...")
st.sidebar.info("Transitioning to Autonomous Space Systems Engineer Protocol.")

# -------------------------------
# Main Logic
# -------------------------------
sats = get_satellites()

if sats:
    ts = load.timescale()
    t0 = ts.now()

    sat_data = []
    # Using a safe limit of 50 for rapid cloud performance
    processed_sats = sats[:50] 

    # -------------------------------
    # Get current positions
    # -------------------------------
    for sat in processed_sats:
        try:
            geocentric = sat.at(t0)
            subpoint = wgs84.subpoint(geocentric)
            pos_km = geocentric.position.km

            sat_data.append({
                "Name": sat.name,
                "Lat": subpoint.latitude.degrees,
                "Lon": subpoint.longitude.degrees,
                "Alt": subpoint.elevation.km,
                "Object": sat,
                "Pos_XYZ": pos_km
            })
        except:
            continue

    df = pd.DataFrame(sat_data)

    # -------------------------------
    # Conjunction Analysis (TCA + Probability)
    # -------------------------------
    st.subheader("⚠️ Conjunction Risk Analysis")

    alerts = []
    # Predict next 30 minutes in 5-minute increments
    time_range = [t0 + (i * 5 / 1440.0) for i in range(6)]

    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            sat_i = df.iloc[i]["Object"]
            sat_j = df.iloc[j]["Object"]
            
            min_dist = 9999.0
            tca_time = ""

            for t in time_range:
                try:
                    p_i = sat_i.at(t).position.km
                    p_j = sat_j.at(t).position.km
                    d = np.linalg.norm(p_i - p_j)
                    
                    if d < min_dist:
                        min_dist = d
                        tca_time = t.utc_strftime('%H:%M:%S')
                except:
                    continue

            # If objects are within 1000km, show a risk analysis
            if min_dist < 1000:
                pc = collision_probability(min_dist)
                alerts.append({
                    "Pair": f"{sat_i.name} / {sat_j.name}",
                    "MinDist": f"{min_dist:.2f} km",
                    "TCA": tca_time,
                    "Risk": f"{pc:.6f}"
                })

    if alerts:
        alert_df = pd.DataFrame(alerts)
        st.table(alert_df) # Clean professional table
    else:
        st.success("✅ No high-risk conjunctions detected in current orbital window.")

    # -------------------------------
    # Visualization
    # -------------------------------
    st.subheader("🌍 Live Orbital Map (3D Globe)")

    fig = px.scatter_geo(
        df,
        lat="Lat",
        lon="Lon",
        hover_name="Name",
        projection="orthographic",
        title="Global Satellite Traffic Monitor"
    )

    fig.update_geos(
        showcountries=True,
        showocean=True,
        oceancolor="#000814",
        landcolor="#212529",
        bgcolor="black"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("CelesTrak Data Stream Offline. Standing by for Handshake...")

# -------------------------------
# Footer
# -------------------------------
st.divider()
st.caption("Space Nova Protocol © 2026 | Phase 9: Autonomous Conjunction Intelligence")
