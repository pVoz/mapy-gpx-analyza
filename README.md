# mapy-gpx-analyza
Python aplikácia na analýzu túr z Mapy.cz
# 🗺️ GPX Analyzer – Analýza trás z Mapy.cz

Python aplikácia na spracovanie a vizualizáciu turistických trás exportovaných z [Mapy.cz](https://mapy.cz).  
Analyzuje vzdialenosť, prevýšenie, kreslí výškový profil a ukladá dáta do databázy.

---

## 🚀 Funkcie

- ✅ Načítanie `.gpx` súborov
- ✅ Výpočet vzdialenosti, stúpania a klesania
- ✅ Vizualizácia trasy na mape (`folium`)
- ✅ Vykreslenie výškového profilu (`matplotlib`)
- ✅ Ukladanie údajov do databázy (`sqlite3`)
- ✅ Export mapy do HTML a grafu do PNG
- 📦 (v pláne) Export do `.csv` / `.json`, webové rozhranie

---

## 🛠️ Inštalácia

1. Naklonuj si repozitár:
   ```bash
   git clone https://github.com/pVoz/mapy-gpx-analyza.git
   cd mapy-gpx-analyza
