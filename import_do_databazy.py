import json
import sqlite3

# Načítanie JSON súboru
with open("trasy.json", "r", encoding="utf-8") as f:
    data = json.load(f)

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

# Vloženie údajov z JSON do databázy
for trasa in data:
    cursor.execute("""
    INSERT INTO trasy (nazov, vzdialenost, stupanie, klesanie, datum)
    VALUES (?, ?, ?, ?, ?)
    """, (
        trasa["nazov"],
        trasa["vzdialenost_km"],
        trasa["stupanie_m"],
        trasa["klesanie_m"],
        trasa["datum"]
    ))

conn.commit()
conn.close()

print("✅ Údaje boli úspešne importované do databázy trasy.db")
