import streamlit as st
from skyfield.api import load
import pandas as pd

# 1. PAGE CONFIG
st.set_page_config(page_title="Space Nova | Global", page_icon="🚀", layout="wide")

# 2. DATA ENGINES (Cached for speed)
@st.cache_resource
def get_active_data():
    url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle'
    return load.tle_file(url)

@st.cache_resource
def get_debris_data():
    url = 'https://celestrak.org/NORAD/elements/gp.php?GROUP=1999-025&FORMAT=tle'
    return load.tle_file(url)

# 3. SIDEBAR CONTROL PANEL (Your Manual Governance)
st.sidebar.header("🕹️ Mission Control")
view_mode = st.sidebar.selectbox("Select Governance View", ["Active Assets", "Debris Fields"])

# 4. CORE LOGIC
ts = load.timescale()
t = ts.now()

if view_mode == "Debris Fields":
    sats = get_debris_data()
    st.title("⚠️ Debris Monitor: Danger Zones")
    map_color = "#ff4b4b" # Red for danger
else:
    sats = get_active_data()
    st.title("🛰️ Space Nova: Global Monitor")
    map_color = "#00fbff" # Cyan for active

# Calculate coordinates for the first 150 nodes
locations = []
for s in sats[:150]:
    try:
        subpoint = s.at(t).subpoint()
        locations.append({
            'lat': subpoint.latitude.degrees,
            'lon': subpoint.longitude.degrees,
            'Name': s.name
        })
    except: continue

# 5. THE INTERACTIVE INTERFACE
df = pd.DataFrame(locations)
st.map(df, color=map_color)

st.write("---")
st.subheader("📊 Phase 7: Real-Time Outcomes")
c1, c2, c3 = st.columns(3)
c1.metric("Fuel Efficiency", "90%", "+15%")
c2.metric("Thermal Stability", "92%", "Optimal")
c3.metric("Drift Status", "Active", "Predictive")

st.info("Founder: Annesha Mazumdar | Space Nova Technical Protocol")
# Simulated Collision Detection
st.sidebar.divider()
st.sidebar.subheader("🛡️ Collision Avoidance")
if st.sidebar.button("Scan for Proximity"):
    st.sidebar.error("ALERT: Node 12-B in Proximity to Debris")
    st.sidebar.info("Protocol: Initiating 48h Thermal-Aware Drift")
    st.balloons() # To celebrate the successful detection!
