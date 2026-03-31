import streamlit as st
import pandas as pd
import numpy as np
from skyfield.api import load, wgs84
from datetime import timedelta
import plotly.express as px

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Space Nova Protocol: Phase 9", layout="wide")

# -------------------------------
# Load Satellite Data
# -------------------------------
@st.cache_resource
def get_satellites():
    url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
    try:
        return load.tle_file(url)
    except:
        return None

# -------------------------------
# Collision Probability Model
# -------------------------------
def collision_probability(dist_km):
    sigma = 2  # uncertainty radius (km)
    return np.exp(-(dist_km**2) / (2 * sigma**2))

# -------------------------------
# UI Header
# -------------------------------
st.title("🚀 Space Nova: Autonomous Orbital Intelligence (Phase 9)")
st.markdown("### Decision-Grade Conjunction Analysis + TCA + Collision Risk")

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.header("System Status: OPERATIONAL")
st.sidebar.success("Mode: Advanced Conjunction Analysis Active")
st.sidebar.warning("Scanning future orbital paths...")

# -------------------------------
# Main Logic
# -------------------------------
sats = get_satellites()

if sats:
    ts = load.timescale()
    t0 = ts.now()

    sat_data = []
    processed_sats = sats[:60]  # limit for performance

    # -------------------------------
    # Get current positions
    # -------------------------------
    for sat in processed_sats:
        try:
            geocentric = sat.at(t0)
            subpoint = wgs84.subpoint(geocentric)

            sat_data.append({
                "Name": sat.name,
                "Lat": subpoint.latitude.degrees,
                "Lon": subpoint.longitude.degrees,
                "Alt": subpoint.elevation.km,
                "Object": sat
            })
        except:
            continue

    df = pd.DataFrame(sat_data)

    # -------------------------------
    # Conjunction Analysis (ADVANCED)
    # -------------------------------
    st.subheader("⚠️ Conjunction Risk Analysis (TCA + Probability)")

    alerts = []

    # Create time range (next 60 minutes)
    time_range = [t0 + i/1440 for i in range(0, 60)]

    for i in range(len(df)):
        for j in range(i + 1, len(df)):

            sat_i = df.iloc[i]["Object"]
            sat_j = df.iloc[j]["Object"]

            min_dist = float('inf')
            tca_time = None
            closing_speed_final = None

            for t in time_range:
                try:
                    pos_i = sat_i.at(t).position.km
                    pos_j = sat_j.at(t).position.km

                    vel_i = sat_i.at(t).velocity.km_per_s
                    vel_j = sat_j.at(t).velocity.km_per_s

                    rel_pos = pos_i - pos_j
                    rel_vel = vel_i - vel_j

                    dist = np.linalg.norm(rel_pos)

                    if dist < min_dist:
                        min_dist = dist
                        tca_time = t.utc_iso()

                        # Compute closing speed
                        closing_speed = np.dot(rel_vel, rel_pos)
                        closing_speed_final = closing_speed

                except:
                    continue

            # -------------------------------
            # Final Risk Check
            # -------------------------------
            if min_dist < 10 and closing_speed_final is not None and closing_speed_final < 0:
                pc = collision_probability(min_dist)

                alerts.append(
                    f"⚠️ {sat_i.name} vs {sat_j.name} | "
                    f"MinDist: {min_dist:.2f} km | "
                    f"TCA: {tca_time} | "
                    f"Pc: {pc:.6f}"
                )

    # -------------------------------
    # Display Alerts
    # -------------------------------
    if alerts:
        for alert in alerts[:5]:
            st.error(alert)
    else:
        st.success("✅ No immediate high-risk conjunctions detected.")

    # -------------------------------
    # Visualization
    # -------------------------------
    st.subheader("🌍 Live Orbital Map")

    fig = px.scatter_geo(
        df,
        lat="Lat",
        lon="Lon",
        hover_name="Name",
        projection="orthographic",
        title="Live Global Orbital Traffic
