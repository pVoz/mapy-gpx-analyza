import sqlite3

EVEREST_VYSKA = 8848  # m

# Pripojenie k databáze
conn = sqlite3.connect("trasy.db")
cursor = conn.cursor()

# Spočítanie všetkých výškových metrov a kilometrov
cursor.execute("SELECT SUM(stupanie), SUM(vzdialenost) FROM trasy")
stupanie_spolu, vzdialenost_spolu = cursor.fetchone()

conn.close()

# Ochrana pred None
stupanie_spolu = stupanie_spolu or 0
vzdialenost_spolu = vzdialenost_spolu or 0

# Výpočet pokroku
percenta = min(100, (stupanie_spolu / EVEREST_VYSKA) * 100)

print(f"🧭 Tvoja cesta na Mount Everest:")
print(f"   ➤ Výškové metre: {stupanie_spolu:.0f} m z {EVEREST_VYSKA} m")
print(f"   ➤ Prejdené kilometre: {vzdialenost_spolu:.2f} km")
print(f"   ➤ Postup: {percenta:.2f} %")

if stupanie_spolu >= EVEREST_VYSKA:
    print("🎉 Gratulujem! Symbolicky si dosiahol vrchol Mount Everestu!")
else:
    zostava = EVEREST_VYSKA - stupanie_spolu
    print(f"   ➤ Zostáva {zostava:.0f} výškových metrov")
