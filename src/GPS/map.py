import folium
import pandas as pd

def generate_map():

    data = pd.read_csv("GPS/save_data/GPS.csv", name=["gas", "temperature", "pressure","humidity"])

    m = folium.Map(location=[data, data.mean()])

    for _, row in data.iterrows():
        color = "green" if row.gas > 100000 else "red"

        folium.CircleMarker(
            location=[row.lat, row.lon],
            radius=8,
            color=color,
            fill=True,
            fill_color=color,
            popup=f"Gas: {row.gas}"
        ).add_to(m)

    m.save("airpurifier.html")