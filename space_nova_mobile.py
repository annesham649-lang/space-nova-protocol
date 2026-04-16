import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Space Nova | Autonomous Executive", layout="wide", initial_sidebar_state="collapsed")

# --- HIGH-END CYBERPUNK CSS ---
st.markdown("""
    <style>
    /* Main Background */
    .main { background: radial-gradient(circle, #050510 0%, #000000 100%); color: #00f5d4; }
    
    /* Neon Metric Cards */
    div[data-testid="stMetricValue"] { color: #00f5d4 !important; font-family: 'Courier New'; font-weight: bold; }
    div[data-testid="stMetricLabel"] { color: #8892b0 !important; font-family: 'Verdana'; }
    
    /* Glassmorphism Effect for Tables */
    div[data-testid="stTable"] { 
        background: rgba(10, 10, 32, 0.7); 
        border-radius: 15px; 
        border: 1px solid rgba(0, 245, 212, 0.2);
        padding: 10px;
    }
    
    /* Custom Headers */
    h1, h2, h3 { 
        color: #00f5d4 !important; 
        text-shadow: 0px 0px 15px rgba(0, 245, 212, 0.6); 
        font-family: 'Courier New', Courier, monospace; 
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Pulse Animation for Status */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    .status-pulse { color: #00ff00; animation: pulse 2s infinite; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.write(f"**SYSTEM STATUS:** <span class='status-pulse'>ACTIVE - PHASE 10 PROTOCOL</span>", unsafe_allow_html=True)
st.title("🛰️ SPACE NOVA | AUTONOMOUS COMMAND")
st.markdown("---")

# --- EXECUTIVE METRICS (The Dashboard Header) ---
cols = st.columns(4)
cols[0].metric("ASSETS TRACKED", "1,204", "NOMINAL")
cols[1].metric("LATENCY", "0.004s", "OPTIMIZED")
cols[2].metric("COLLISIONS BLOCKED", "14", "+2 THIS CYCLE")
cols[3].metric("FUEL EFFICIENCY", "98.2%", "MAX LOAD")

# --- 3D NEON GLOBE ENGINE ---
df = pd.DataFrame({
    "Name": [f"NOVA-{i:02d}" for i in range(1, 13)],
    "Lat": np.random.uniform(-50, 50, 12),
    "Lon": np.random.uniform(-170, 170, 12),
    "Health": ["Stable" for _ in range(12)]
})

fig = go.Figure()

# Add the Satellite Nodes with a "Glow"
fig.add_trace(go.Scattergeo(
    lat=df['Lat'], lon=df['Lon'],
    mode='markers+text',
    text=df['Name'],
    textposition="top center",
    marker=dict(
        size=12,
        color='#00f5d4',
        opacity=1,
        line=dict(width=2, color='#ffffff'),
        symbol='diamond'
    ),
    hoverinfo='text'
))

fig.update_geos(
    projection_type="orthographic",
    showocean=True, oceancolor="#020205",
    showland=True, landcolor="#0a0a20",
    showcountries=True, countrycolor="#1c2541",
    bgcolor="rgba(0,0,0,0)",
    showframe=False,
    projection_rotation=dict(lon=88, lat=20, roll=0)
)

fig.update_layout(
    height=700, margin={"r":0,"t":0,"l":0,"b":0},
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#00f5d4")
)

st.plotly_chart(fig, use_container_width=True)

# --- TWO-COLUMN COMMAND CENTER ---
left_col, right_col = st.columns([1, 1])

with left_col:
    st.markdown("### ⚡ REAL-TIME MANEUVERS")
    risks = pd.DataFrame({
        "ASSET ID": df['Name'].head(6),
        "ACTION": ["STABLE", "STABLE", "NUDGE EXECUTED", "STABLE", "ADJUSTING", "STABLE"],
        "CONFIDENCE": ["99.8%", "99.9%", "94.2%", "99.9%", "88.5%", "99.9%"]
    })
    st.table(risks)

with right_col:
    st.markdown("### 🧠 AUTONOMOUS LOGS")
    log_data = {
        "TIMESTAMP": [datetime.now().strftime("%H:%M:%S") for _ in range(6)],
        "EVENT": [
            "Syncing with Celestrak Feed...",
            "Collision Probability < 0.00001%",
            "Anomaly Detected: NOVA-03",
            "Maneuver Calculated (0.004s)",
            "Propulsion Optimization applied",
            "Fleet Status: All Nodes Nominal"
        ]
    }
    st.table(pd.DataFrame(log_data))

st.divider()
st.caption("Space Nova Executive Protocol © 2026 | Digital Architect: Annesha Mazumdar")
