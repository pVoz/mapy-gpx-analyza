import gpxpy
import gpxpy.gpx
import folium
import sqlite3
import matplotlib.pyplot as plt
from datetime import date
from math import sqrt

def distance(point1, point2):
    # Vzdialenosť medzi dvoma bodmi na základe zemepisnej šírky a dĺžky (v metroch)
    return point1.distance_3d(point2)

# Načítanie GPX súboru
with open("trasa1.gpx", "r", encoding="utf-8") as gpx_file:
    gpx = gpxpy.parse(gpx_file)

total_distance = 0.0  # v metroch
total_uphill = 0.0    # v metroch
total_downhill = 0.0  # v metroch

for track in gpx.tracks:
    for segment in track.segments:
        previous_point = None
        for point in segment.points:
            if previous_point:
                dist = distance(previous_point, point)
                total_distance += dist

                elevation_diff = point.elevation - previous_point.elevation
                if elevation_diff > 0:
                    total_uphill += elevation_diff
                else:
                    total_downhill += abs(elevation_diff)

            previous_point = point

print(f"Celková vzdialenosť: {total_distance/1000:.2f} km")
print(f"Stúpanie: {total_uphill:.0f} m")
print(f"Klesanie: {total_downhill:.0f} m")

# Získame všetky GPS body trasy
points = []

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            points.append((point.latitude, point.longitude))

# Vytvorenie mapy – stred mapy dáme na prvý bod
start_coords = points[0]
m = folium.Map(location=start_coords, zoom_start=13)

# Pridáme trasu ako čiaru
folium.PolyLine(points, color="blue", weight=4.5, opacity=0.9).add_to(m)

# Pridáme značku na začiatok a koniec
folium.Marker(points[0], popup="Štart", icon=folium.Icon(color='green')).add_to(m)
folium.Marker(points[-1], popup="Cieľ", icon=folium.Icon(color='red')).add_to(m)

# Uložíme mapu do HTML súboru
m.save("trasa_mapa.html")
print("Mapa uložená ako trasa_mapa.html")

# Pripojenie k databáze (vytvorí sa, ak neexistuje)
conn = sqlite3.connect("trasy.db")
cursor = conn.cursor()

# Vytvorenie tabuľky, ak ešte neexistuje
cursor.execute("""
CREATE TABLE IF NOT EXISTS trasy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nazov TEXT,
    vzdialenost REAL,
    stupanie INTEGER,
    klesanie INTEGER,
    datum TEXT
)
""")

# Vloženie údajov o trase
nazov_trasy = "Moja prvá túra"
datum_dnes = date.today().isoformat()

cursor.execute("""
INSERT INTO trasy (nazov, vzdialenost, stupanie, klesanie, datum)
VALUES (?, ?, ?, ?, ?)
""", (nazov_trasy, total_distance / 1000, int(total_uphill), int(total_downhill), datum_dnes))

conn.commit()
conn.close()

print("Trasa uložená do databázy.")


# Získame zoznam výšok a vzdialeností
elevations = []
distances = []

cumulative_distance = 0.0
previous_point = None

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            if previous_point:
                dist = point.distance_3d(previous_point)
                cumulative_distance += dist
            elevations.append(point.elevation)
            distances.append(cumulative_distance / 1000)  # v kilometroch
            previous_point = point

# Vykreslenie grafu
plt.figure(figsize=(10, 5))
plt.plot(distances, elevations, color='green')
plt.title("Výškový profil trasy")
plt.xlabel("Vzdialenosť (km)")
plt.ylabel("Nadmorská výška (m)")
plt.grid(True)
plt.tight_layout()
plt.savefig("vyskovy_profil.png")  # uloženie grafu
plt.show()  # zobrazenie grafu