### 🌲 Eco-Surveillance Spatial Threat Matrix Dashboard

An event-driven, cloud-native geospatial dashboard designed for real-time environmental monitoring and tactical wilderness protection.

This repository hosts a lightweight, serverless Python web application built with **Streamlit** and **Folium (Leaflet.js)** that acts as a centralized Command & Control interface for field operations. It visualizes acoustic threat telemetry (such as illegal logging, poaching, or unauthorized vehicles) processed upstream by AI analytics and orchestrated via n8n.

#### 🚀 Key Capabilities:

* **Real-Time Geospatial Heatmaps:** Dynamically renders an interactive, dark-theme satellite map displaying localized threat density and hotspots based on live coordinate telemetry.
* **Serverless Cloud Data Architecture:** Decoupled entirely from local infrastructure, reading live streaming incident logs directly from a cloud-managed Google Sheets CSV endpoint via asynchronous HTTP requests.
* **On-Demand Telemetry Synchronization:** Features cache-busting manual refresh triggers to immediately fetch and parse the latest edge sensor alerts.
* **Historical Audit Feed:** Provides an interactive, chronological data grid sorting historical threat vectors, severity classifications, and AI-generated tactical summaries for post-incident review.

#### 🛠️ Tech Stack:

* **Frontend/Hosting:** Streamlit Cloud
* **Geospatial Visualization:** Folium, Leaflet.js, Streamlit-Folium
* **Data Processing:** Pandas (Python)
* **Data Pipeline Pipeline (Upstream):** n8n, Gemini 2.5 Flash, Google Sheets API
