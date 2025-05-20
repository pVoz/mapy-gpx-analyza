import sqlite3
import csv

# Pripojenie k databáze
conn = sqlite3.connect("trasy.db")
cursor = conn.cursor()

# Získanie údajov
cursor.execute("SELECT id, nazov, vzdialenost, stupanie, klesanie, datum FROM trasy")
trasy = cursor.fetchall()

# Export do CSV s BOM a bodkočiarkami ako oddeľovačmi
with open("trasy.csv", "w", newline="", encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    
    # Hlavička
    writer.writerow(["ID", "Názov", "Vzdialenosť (km)", "Stúpanie (m)", "Klesanie (m)", "Dátum"])
    
    # Údaje
    for t in trasy:
        writer.writerow([
            t[0],
            t[1],
            round(t[2], 2),
            t[3],
            t[4],
            t[5]
        ])

conn.close()
print("✅ CSV bolo uložené s bodkočiarkami ako oddeľovačmi (trasy.csv)")
