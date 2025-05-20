import sqlite3
import matplotlib.pyplot as plt

# 🗻 Everest výškový profil (názvy + výška v m)
everest_profile = [
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
]

# Vytvor os X (0,1,2...) a Y (výšky)
etapy = list(range(len(everest_profile)))
vysky = [bod[1] for bod in everest_profile]
nazy = [bod[0] for bod in everest_profile]
EVEREST_VYSKA = vysky[-1]

# 🔍 Spočítaj stúpanie používateľa
conn = sqlite3.connect("trasy.db")
cursor = conn.cursor()
cursor.execute("SELECT SUM(stupanie) FROM trasy")
stupanie_spolu = cursor.fetchone()[0] or 0
conn.close()

# 🔼 Nájdeme, v ktorom úseku sa používateľ nachádza
pozicia_idx = 0
for i, vyska in enumerate(vysky):
    if stupanie_spolu < vyska:
        pozicia_idx = i - 1 if i > 0 else 0
        break
else:
    pozicia_idx = len(vysky) - 1

# 💯 Percento výstupu
percento = min(100, (stupanie_spolu / EVEREST_VYSKA) * 100)
zostava = max(0, EVEREST_VYSKA - stupanie_spolu)

# 🎨 Graf
plt.figure(figsize=(14, 6))
plt.plot(etapy, vysky, color="saddlebrown", linewidth=2, label="Výstup na Everest")
plt.scatter(pozicia_idx, vysky[pozicia_idx], color="green", s=120, marker="^", label="Tvoja pozícia")

# 🏕️ Označenie každého tábora
for i, (nazov, vyska) in enumerate(everest_profile):
    plt.text(i, vyska + 100, f"{nazov}\n{vyska} m", ha="center", fontsize=8)

# 🎯 Pozícia používateľa
plt.text(pozicia_idx, vysky[pozicia_idx] - 250,
         f"{stupanie_spolu:.0f} m\n({percento:.1f} %)", 
         ha="center", fontsize=10, color="green", fontweight="bold")

# 📋 Dizajn grafu
plt.title("🧗‍♂️ Tvoj výstup na Mount Everest", fontsize=16, weight='bold')
plt.ylabel("Nadmorská výška (m)")
plt.xticks(etapy, [f"{i+1}" for i in etapy])
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()

# 💾 Uloženie + zobrazenie
plt.savefig("everest_progress_3d_like.png")
plt.show()
