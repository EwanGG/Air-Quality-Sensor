import streamlit as st
import pandas as pd
import sqlite3
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Air Quality Monitor", layout="wide")
st_autorefresh(interval=5000, key="datarefresh") # Auto-refresh every 5s

def load_data():
    conn = sqlite3.connect('air_quality.db')
    # Get the last 50 readings
    query = "SELECT * FROM sensor_data ORDER BY reading_time DESC LIMIT 50"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

st.title("(Real-Time Air Quality Dashboard)")

df = load_data()

if not df.empty:
    # 1. Top Metrics
    latest = df.iloc[0]
    c1, c2, c3 = st.columns(3)
    c1.metric("Temperature", f"{latest['temperature']:.1f}°C")
    c2.metric("Humidity", f"{latest['humidity']:.1f}%")
    c3.metric("Gas Resistance", f"{int(latest['gas'])} Ω")

    # 2. Temperature Trend
    st.subheader("Temperature Over Time")
    # We use reading_time for the X-axis
    st.line_chart(df.set_index('reading_time')['temperature'])

    # 3. Map (Only shows if GPS has fix)
    if latest['latitude'] is not None:
        st.subheader("Sensor Location")
        st.map(df.dropna(subset=['latitude', 'longitude']))
else:
    st.info("Waiting for data to populate in air_quality.db...")