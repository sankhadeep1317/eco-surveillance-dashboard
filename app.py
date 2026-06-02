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

try:
    # Pull fresh streaming database rows over live HTTP
    df = pd.read_csv(SHEET_CSV_URL)
    
    # Cast coordinate data types safely to float
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df = df.dropna(subset=['latitude', 'longitude'])

    # 📊 SECTION 1: Top-Level KPI Analytics Cards
    total_logs = len(df)
    active_threats = len(df[df['threat_type'].str.upper() != 'NONE'])
    critical_alerts = len(df[df['severity'].str.upper() == 'HIGH'])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="📡 Total Pings Logged", value=total_logs)
    with col2:
        st.metric(label="⚠️ Active Threats Identified", value=active_threats, 
                  delta=f"{active_threats} anomalies" if active_threats > 0 else None, delta_color="inverse")
    with col3:
        st.metric(label="🚨 High Severity Escalations", value=critical_alerts)
    with col4:
        # Quick manual refresh button aligned right next to the metrics
        if st.button("🔄 Sync Live Telemetry", use_container_width=True):
            st.rerun()

    st.markdown("---")

    # 🗺️ SECTION 2: Dynamic Geospatial Layer
    # Center map dynamically to the average location of your sensors, fallback if empty
    center_lat = df['latitude'].mean() if not df.empty else 18.8
    center_lon = df['longitude'].mean() if not df.empty else 74.8
    
    base_map = folium.Map(location=[center_lat, center_lon], zoom_start=9, tiles="CartoDB dark_matter")
    
    # 1. Overlay the Macro Heatmap for threat density
    heat_df = df[df['threat_type'].str.upper() != 'NONE'][['latitude', 'longitude']]
    if not heat_df.empty:
        HeatMap(heat_df.values.tolist(), radius=25, blur=15, min_opacity=0.4).add_to(base_map)

    # 2. Plot Individual Color-Coded Incident Circles with AI Summary Popups
    for _, row in df.iterrows():
        threat = str(row['threat_type']).upper()
        severity = str(row['severity']).upper()
        
        # Determine marker coloration based on environmental risk profile
        if threat == "NONE":
            marker_color = "#2ecc71"  # Soft Green for baseline biodiversity
        elif severity == "HIGH":
            marker_color = "#e74c3c"  # Crisp Red for critical immediate hazards
        elif severity == "MEDIUM":
            marker_color = "#f39c12"  # Vivid Orange for intermediate machinery signatures
        else:
            marker_color = "#3498db"  # Blue for low-risk anomalies

        # Construct clean HTML layout inside the clickable popup panel
        popup_html = f"""
        <div style="font-family: 'Helvetica Neue', Arial, sans-serif; width: 260px; font-size: 13px; color: #2c3e50;">
            <h4 style="margin: 0 0 5px 0; color: {marker_color}; font-weight: bold;">🚨 ALERT: {threat}</h4>
            <b>Sector:</b> {row['zone']} (ID: {row['sensor_id']})<br>
            <b>Severity:</b> <span style="color: {marker_color}; font-weight: bold;">{severity}</span><br>
            <b>Confidence:</b> {float(row['confidence'])*100:.1f}%<br>
            <p style="margin: 8px 0 0 0; font-size: 11px; line-height: 1.4; color: #7f8c8d; border-top: 1px solid #ecf0f1; padding-top: 5px;">
                {row['summary'][:200]}...
            </p>
        </div>
        """
        
        # Bind the data payload to the individual Leaflet node layer
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=8 if threat != "NONE" else 5,
            color=marker_color,
            fill=True,
            fill_color=marker_color,
            fill_opacity=0.7,
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(base_map)

    # Render interactive map component on the web dashboard page
    st_folium(base_map, width=1400, height=600, returned_objects=[])
    
    # 📋 SECTION 3: Historical Audit Feed Log Drawer
    st.subheader("📋 Historical Incident Feed Log")
    st.dataframe(df.sort_index(ascending=False), use_container_width=True)

except Exception as e:
    st.info("Awaiting live edge telemetry data stream connection... Click sync to check.")
    st.error(f"System Log Diagnostics: {e}")
