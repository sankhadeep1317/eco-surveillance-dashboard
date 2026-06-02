import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap

# Configure wide-screen display layouts
st.set_page_config(layout="wide", page_title="Eco-Surveillance Command Center")
st.title("🌲 Live Spatial Threat Matrix Dashboard")

# 🚨 PASTE YOUR COPIED GOOGLE SHEETS CSV URL HERE
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTX_XN5-OJLNOs73XPd4RRlog_uxTHDMmRliaZ2URTBUj2L9uhjIbT3Vrtsaxn6Cut5jooITL6Ql3aH/pub?gid=0&single=true&output=csv"

# Add a manual refresh button to fetch the absolute latest telemetry rows
if st.button("🔄 Refresh Map Telemetry"):
    st.rerun()

try:
    # Pull fresh streaming database rows over live HTTP
    df = pd.read_csv(SHEET_CSV_URL)
    
    # Cast coordinate data types safely to float
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df = df.dropna(subset=['latitude', 'longitude'])

    # Initialize dark-theme satellite tactical map centered broadly around your cluster zone
    base_map = folium.Map(location=[18.8, 74.8], zoom_start=8, tiles="CartoDB dark_matter")
    
    # Isolate true positive threat signatures (exclude 'None') to build heat intensity weights
    heat_df = df[df['threat_type'] != 'None'][['latitude', 'longitude']]
    
    if not heat_df.empty:
        heat_data = heat_df.values.tolist()
        # Overlay the mathematical heatmap layer
        HeatMap(heat_data, radius=25, blur=15, min_opacity=0.6).add_to(base_map)

    # Render interactive map canvas 
    st_folium(base_map, width=1400, height=650)
    
    # Show data table log footer
    st.subheader("📋 Historical Incident Feed Log")
    st.dataframe(df.sort_index(ascending=False), use_container_width=True)

except Exception as e:
    st.info("Awaiting live edge telemetry data stream connection... Click refresh to check.")
