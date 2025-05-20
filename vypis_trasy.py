import sqlite3

# Pripojenie k databáze
conn = sqlite3.connect("trasy.db")
cursor = conn.cursor()

# Načítanie všetkých trás
cursor.execute("SELECT id, nazov, vzdialenost, stupanie, klesanie, datum FROM trasy")
vysledky = cursor.fetchall()

# Výpis
print("\nZoznam uložených trás:")
print("-" * 40)
for trasa in vysledky:
    print(f"ID: {trasa[0]}")
    print(f"Názov: {trasa[1]}")
    print(f"Vzdialenosť: {trasa[2]:.2f} km")
    print(f"Stúpanie: {trasa[3]} m")
    print(f"Klesanie: {trasa[4]} m")
    print(f"Dátum: {trasa[5]}")
    print("-" * 40)

conn.close()
