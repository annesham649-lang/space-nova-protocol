import streamlit as st
import pandas as pd
from skyfield.api import load, wgs84
from datetime import datetime, timedelta
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Space Nova Protocol: Phase 8", layout="wide")

@st.cache_resource
def get_active_data():
    url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=visual&FORMAT=tle'
    try:
        return load.tle_file(url, reload=True)
    except:
        return None

# --- UI Header ---
st.title("🛰️ Space Nova: Autonomous Governance (Phase 8)")
st.markdown("### Decision-Grade Conjunction Analysis & Orbital Safety")

# --- Sidebar ---
st.sidebar.header("System Status: OPERATIONAL")
st.sidebar.info("Mode: Conjunction Analysis Active")
st.sidebar.warning("Scanning for Potential Collisions...")

# --- Main Logic ---
sats = get_active_data()

if sats:
    ts = load.timescale()
    t = ts.now()
    
    sat_positions = []
    processed_sats = sats[:80] # Limit for performance speed

    for sat in processed_sats:
        try:
            geocentric = sat.at(t)
            subpoint = wgs84.subpoint(geocentric)
            # Get 3D coordinates for distance math
            pos = geocentric.position.km
            sat_positions.append({
                "Name": sat.name,
                "Lat": subpoint.latitude.degrees,
                "Lon": subpoint.longitude.degrees,
                "Alt": subpoint.elevation.km,
                "Pos_XYZ": pos
            })
        except:
            continue

    df = pd.DataFrame(sat_positions)

    # --- PHASE 8: CONJUNCTION ANALYSIS (The "Top 1%" Logic) ---
    st.subheader("⚠️ Close Approach & Collision Warnings")
    alerts = []
    
    # Compare each satellite to others to find distance
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            dist = np.linalg.norm(df.iloc[i]['Pos_XYZ'] - df.iloc[j]['Pos_XYZ'])
            if dist < 500: # Threshold in Kilometers
                alerts.append(f"ALERT: {df.iloc[i]['Name']} & {df.iloc[j]['Name']} | Distance: {int(dist)}km")

    if alerts:
        for alert in alerts[:5]: # Show top 5 threats
            st.error(alert)
    else:
        st.success("No immediate conjunction threats detected in current orbit.")

    # --- Visualization ---
    fig = px.scatter_geo(df, lat='Lat', lon='Lon', hover_name='Name',
                        projection="orthographic", # "Globe" view looks more professional
                        title="Live Global Orbital Traffic")
    
    fig.update_geos(showcountries=True, projection_type="orthographic", showocean=True, oceancolor="black", landcolor="grey")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("CelesTrak Database is updating. The Space Nova engine is standing by...")

st.divider()
st.caption("Space Nova Protocol © 2026 | Transitioning to Autonomous Space Systems")
