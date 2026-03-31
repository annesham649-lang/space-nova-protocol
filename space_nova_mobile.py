import streamlit as st
import pandas as pd
from skyfield.api import load, wgs84
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="Space Nova Global Monitor", layout="wide")

@st.cache_resource
def get_active_data():
    # Using 'visual' group for faster cloud loading
    url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=visual&FORMAT=tle'
    try:
        # Load the satellite data
        satellites = load.tle_file(url, reload=True)
        return satellites
    except Exception as e:
        return None

# --- UI Header ---
st.title("🌌 Space Nova: Global Orbital Monitor")
st.markdown("### Phase 7: Real-Time Governance & Sustainability Tracking")

# --- Sidebar Metrics ---
st.sidebar.header("Satellite Status")
st.sidebar.metric("Fuel Reserve", "90%", "+2%")
st.sidebar.metric("Thermal Shield", "92%", "Stable")
st.sidebar.info("Operational Mode: Active Governance")

# --- Main Logic ---
sats = get_active_data()

if sats:
    ts = load.timescale()
    t = ts.now()
    
    sat_data = []
    # Process first 100 satellites for performance
    for sat in sats[:100]:
        try:
            geocentric = sat.at(t)
            subpoint = wgs84.subpoint(geocentric)
            sat_data.append({
                "Name": sat.name,
                "Lat": subpoint.latitude.degrees,
                "Lon": subpoint.longitude.degrees,
                "Alt": subpoint.elevation.km
            })
        except:
            continue

    df = pd.DataFrame(sat_data)

    # Create the Map
    fig = px.scatter_geo(df,
                        lat='Lat',
                        lon='Lon',
                        hover_name='Name',
                        projection="natural earth",
                        title="Live Satellite Positions")
    
    fig.update_geos(showcoastlines=True, coastlinecolor="RebeccaPurple",
                    showland=True, landcolor="LightGreen",
                    showocean=True, oceancolor="LightBlue")

    st.plotly_chart(fig, use_container_width=True)
    st.success(f"Tracking {len(df)} active objects in real-time.")
else:
    st.error("Space Database (Celestrak) is currently busy. Please refresh the page in a few moments.")

st.divider()
st.caption("Space Nova Protocol © 2026 | Empowering Orbital Sustainability")
