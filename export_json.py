import sqlite3
import json

# Pripojenie k databáze
conn = sqlite3.connect("trasy.db")
cursor = conn.cursor()

# Načítanie všetkých trás
cursor.execute("SELECT id, nazov, vzdialenost, stupanie, klesanie, datum FROM trasy")
trasy = cursor.fetchall()

# Prevod na zoznam slovníkov
trasy_json = []
for t in trasy:
    trasa_dict = {
        "id": t[0],
        "nazov": t[1],
        "vzdialenost_km": round(t[2], 2),
        "stupanie_m": t[3],
        "klesanie_m": t[4],
        "datum": t[5]
    }
    trasy_json.append(trasa_dict)

# Uloženie do JSON súboru
with open("trasy.json", "w", encoding="utf-8") as f:
    json.dump(trasy_json, f, ensure_ascii=False, indent=4)

print("✅ Údaje boli exportované do súboru trasy.json")
