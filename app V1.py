import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import matplotlib.pyplot as plt

# ----- Nastavenie výškového profilu -----
hory = {
    "Mount Everest": [
        ("Base Camp", 5364),
        ("Icefall", 5800),
        ("Camp I", 6065),
        ("Western Cwm", 6200),
        ("Camp II", 6400),
        ("Lhotse Face", 6700),
        ("Camp III", 7200),
        ("Camp IV", 7900),
        ("Balcony", 8400),
        ("Summit", 8848),
    ],
    # Tu môžeme neskôr doplniť ďalšie hory
}

# ----- Výber cieľa -----
st.title("🧗‍♂️ Virtuálny výstup na vrchol")
vybrana_hora = st.selectbox("Vyber si cieľovú horu", list(hory.keys()))
profil = hory[vybrana_hora]
etapy = list(range(len(profil)))
vysky = [v[1] for v in profil]
nazy = [v[0] for v in profil]
CIELOVA_VYSKA = vysky[-1]

# ----- Načítanie údajov z databázy -----
conn = sqlite3.connect("trasy.db")
cursor = conn.cursor()
cursor.execute("SELECT SUM(stupanie), SUM(vzdialenost) FROM trasy")
stupanie_spolu, vzdialenost_spolu = cursor.fetchone()
conn.close()

stupanie_spolu = stupanie_spolu or 0
vzdialenost_spolu = vzdialenost_spolu or 0
percento = min(100, (stupanie_spolu / CIELOVA_VYSKA) * 100)
zostava = max(0, CIELOVA_VYSKA - stupanie_spolu)

# ----- Vizualizácia grafu -----
pozicia_idx = 0
for i, vyska in enumerate(vysky):
    if stupanie_spolu < vyska:
        pozicia_idx = i - 1 if i > 0 else 0
        break
else:
    pozicia_idx = len(vysky) - 1

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(etapy, vysky, color="saddlebrown", linewidth=2)
ax.scatter(pozicia_idx, vysky[pozicia_idx], color="green", s=120, marker="^")
for i, (nazov, vyska) in enumerate(profil):
    ax.text(i, vyska + 80, f"{nazov}\n{vyska} m", ha="center", fontsize=8)
ax.text(pozicia_idx, vysky[pozicia_idx] - 300,
        f"{stupanie_spolu:.0f} m\n({percento:.1f} %)",
        ha="center", fontsize=9, color="green", fontweight="bold")
ax.set_ylabel("Nadmorská výška (m)")
ax.set_title(f"Tvoj výstup na {vybrana_hora}", fontsize=14, weight='bold')
ax.grid(True, linestyle="--", alpha=0.5)
st.pyplot(fig)

# ----- Textový výstup -----
st.markdown(f"""
### 📊 Tvoje štatistiky:
- **Prejdené výškové metre:** {int(stupanie_spolu)} m
- **Cieľ:** {CIELOVA_VYSKA} m ({vybrana_hora})
- **Postup:** {percento:.1f} %
- **Zostáva:** {int(zostava)} m
- **Prejdené km:** {vzdialenost_spolu:.2f} km
""")
import streamlit.components.v1 as components

import streamlit as st
import streamlit.components.v1 as components

st.markdown("### 🗺️ Mount Everest 3D pohľad (Cesium)")
with open("cesium_everest.html", "r", encoding="utf-8") as f:
    html = f.read()
components.html(html, height=600)
