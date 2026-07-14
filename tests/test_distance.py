from generator.utils import load_comuni
from generator.distance import haversine_distance

comuni = load_comuni()

milano = comuni[comuni["comune"] == "Milano"].iloc[0]
roma = comuni[comuni["comune"] == "Roma"].iloc[0]

km = haversine_distance(
    milano["lat"],
    milano["lon"],
    roma["lat"],
    roma["lon"]
)

print(f"Milano -> Roma: {km} km")