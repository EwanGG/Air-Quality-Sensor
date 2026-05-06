import streamlit as st
import pandas as pd
import sqlite3

# Set page configuration
st.set_page_config(page_title="Pi Sensor Dashboard", layout="wide")

st.title("🛰️ Real-Time Sensor Dashboard")


# Function to load data from SQLite
def load_data():
    conn = sqlite3.connect('sensor_data.db')
    # We pull the last 20 entries to show trends
    query = "SELECT * FROM sensor_readings ORDER BY temp DESC LIMIT 20"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# 1. Fetch the data
df = load_data()

if not df.empty:
    # 2. Display 'Live' Metrics (The very latest reading)
    latest = df.iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", f"{latest['temperature']}°C")
    col2.metric("Humidity", f"{latest['humidity']}%")
    col3.metric("Gas Level", f"{latest['gas']} ppm")

    # 3. Create a Time-Series Chart
    st.subheader("Environmental Trends")
    # Streamlit needs the time as the index for charts
    chart_data = df.set_index('timestamp')[['temperature', 'humidity']]
    st.line_chart(chart_data)

    # 4. Display the Map
    st.subheader("Sensor Location")
    # Streamlit looks for columns named 'lat' or 'latitude'
    st.map(df[['latitude', 'longitude']])

    # 5. Show Raw Data Table (optional)
    if st.checkbox("Show Raw Data"):
        st.write(df)
else:
    st.warning("No data found in the database yet!")

# Add a button to manually refresh, or use a timer
if st.button('Refresh Data'):
    st.rerun()