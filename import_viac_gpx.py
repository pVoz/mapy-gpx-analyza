import os
import gpxpy
import sqlite3

# Pripojenie k databáze
conn = sqlite3.connect("trasy.db")
cursor = conn.cursor()

# Vytvorenie tabuľky (ak neexistuje)
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

# Funkcia na spracovanie jedného .gpx súboru
def spracuj_gpx(cesta_k_suboru, nazov_trasy):
    with open(cesta_k_suboru, "r", encoding="utf-8") as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    total_distance = 0.0
    total_uphill = 0.0
    total_downhill = 0.0
    previous_point = None

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                if previous_point:
                    dist = point.distance_3d(previous_point)
                    total_distance += dist

                    elevation_diff = point.elevation - previous_point.elevation
                    if elevation_diff > 0:
                        total_uphill += elevation_diff
                    else:
                        total_downhill += abs(elevation_diff)

                previous_point = point

    # Uloženie do DB
    cursor.execute("""
        INSERT INTO trasy (nazov, vzdialenost, stupanie, klesanie, datum)
        VALUES (?, ?, ?, ?, DATE('now'))
    """, (
        nazov_trasy,
        total_distance / 1000,
        int(total_uphill),
        int(total_downhill)
    ))

# Cesta k priečinku s .gpx súbormi
gpx_priecinok = os.path.join(os.getcwd(), "gpx_soubory")

if not os.path.exists(gpx_priecinok):
    print("❌ Priečinok 'gpx_soubory' neexistuje.")
else:
    print(f"🔍 Načítavam súbory z: {gpx_priecinok}")
    for subor in os.listdir(gpx_priecinok):
        if subor.endswith(".gpx"):
            cesta = os.path.join(gpx_priecinok, subor)
            nazov = os.path.splitext(subor)[0]
            print(f"➡️ Spracovávam: {subor}")
            spracuj_gpx(cesta, nazov)

    conn.commit()
    conn.close()
    print("✅ Všetky GPX súbory boli spracované a uložené do databázy.")
