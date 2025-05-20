from dotenv import load_dotenv
load_dotenv()     # načíta premenné z .env do os.environ
import os
token = os.getenv("CESIUM_TOKEN")



import streamlit as st
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- Definuj profily hôr (baseCampElevation, summitElevation) ---
mountains = {
    "Mount Everest": (5364, 8848),
    "Kilimandžáro": (1890, 5895),
    "Gerlachovský štít": (840, 2655),
    # pridaj ďalšie podľa potreby...
}

# 1) Výber hory v sidebar
st.sidebar.title("Výber hory")
selected = st.sidebar.selectbox("Cieľová hora", list(mountains.keys()))
base_elev, summit_elev = mountains[selected]

# 2) Načítanie dát z DB
conn = sqlite3.connect("trasy.db")
cursor = conn.cursor()
cursor.execute("SELECT SUM(stupanie) FROM trasy")
stupanie_spolu = cursor.fetchone()[0] or 0
conn.close()

# Orez na maximum
stupanie_spolu = min(stupanie_spolu, summit_elev)

# 3) Výpočet percenta
percent = (stupanie_spolu - base_elev) / (summit_elev - base_elev) if stupanie_spolu > base_elev else 0
percent = max(0, min(1, percent))

# 4) Štatistiky
st.title(f"🌄 Virtuálny výstup na {selected}")
st.markdown(f"""
- **Prejdené výškové metre:** {int(stupanie_spolu)} m  
- **Základný tábor (base):** {base_elev} m  
- **Vrchol (summit):** {summit_elev} m  
- **Pokrok:** {percent*100:.1f} %
""")

# 5) Dáta pre 3D rez
x = np.linspace(0, 1, 200)
y = np.interp(x, [0, 1], [base_elev, summit_elev])
t = percent
z = np.interp(t, x, y)

# 6) 3D graf
fig = plt.figure(figsize=(8,5))
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, np.zeros_like(x), y, color="saddlebrown", linewidth=2, label=f"{selected} profil")
ax.scatter([t], [0], [z], color="green", s=50, label=f"Tvoja pozícia: {int(stupanie_spolu)} m")

ax.set_xlabel("Progres (% norm.)")
ax.set_ylabel("")
ax.set_yticks([])
ax.set_zlabel("Nadmorská výška (m)")
ax.set_title(f"Offline 3D rez – {selected}")
ax.legend()
st.pyplot(fig)
