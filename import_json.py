import json

# Načítanie JSON súboru
with open("trasy.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Výpis všetkých trás
print("\nZoznam trás zo súboru:")
print("-" * 40)
for trasa in data:
    print(f"Názov: {trasa['nazov']}")
    print(f"Vzdialenosť: {trasa['vzdialenost_km']} km")
    print(f"Stúpanie: {trasa['stupanie_m']} m")
    print(f"Klesanie: {trasa['klesanie_m']} m")
    print(f"Dátum: {trasa['datum']}")
    print("-" * 40)
