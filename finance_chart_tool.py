import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Einheitliche Farbe mit leichtem Blaustich
color = "#ADD8E6"

# Streamlit-Seiteneinstellungen
st.set_page_config(page_title="Finanzberater-Tool", layout="centered")

# Titel in einer Zeile
st.markdown("<h1 style='text-align: center; color: gold;'>Finanzberater-Tool</h1>", unsafe_allow_html=True)

# Sidebar-Header
st.sidebar.markdown("<h1 style='font-family: Arial; font-weight: bold;'>United Hands Capital</h1>", unsafe_allow_html=True)

# Auswahl des Diagrammtyps oben in der Sidebar
chart_type = st.sidebar.selectbox("Diagrammtyp", ["Kuchendiagramm", "Säulendiagramm", "MindMap"], key="chart_type")

# Eingabefeld für das Gesamtbudget
total_budget = st.sidebar.number_input("Gesamtbudget", min_value=0.0, value=0.0, step=0.1)

# Kategorien und Unterkategorien
categories = {
    "Fixkosten": {"Lebenshaltung": 0.0, "Miete": 0.0, "Versicherungen": 0.0, "Kommunikation": 0.0},
    "Freizeit": {"Urlaub": 0.0, "Hobbies": 0.0, "Anschaffungen": 0.0, "Spaß": 0.0},
    "Rücklagen": {"Riesterrente": 0.0, "Depots": 0.0, "Crypto": 0.0},
    "Sicherheit": {"Notfälle": 0.0, "Unerwartetes": 0.0}
}

# Eingabefelder für Unterkategorien in Dropdown-Menüs
values = []
for category, subcategories in categories.items():
    with st.sidebar.expander(category):
        for subcategory in subcategories:
            categories[category][subcategory] = st.number_input(f"{subcategory}", min_value=0.0, value=0.0, step=0.1)
    values.append(sum(subcategories.values()))

# Berechnung der Differenz zwischen Gesamtbudget und Gesamtausgaben
remaining_budget = total_budget - sum(values)
box_color = "#d4edda" if remaining_budget >= 0 else "#f8d7da"

# Anzeige der verbleibenden Mittel über dem Diagramm
st.markdown(f"<div style='padding: 10px; background-color: {box_color}; border-radius: 5px;'>\n"
            f"<strong>Verbleibendes Budget:</strong> {remaining_budget:.2f} €\n"
            f"</div>", unsafe_allow_html=True)

# Diagramm erstellen
fig, ax = plt.subplots(figsize=(6, 3))  # Kleinere Diagrammgröße
if sum(values) == 0:
    st.warning("Bitte geben Sie mindestens einen positiven Wert ein, um das Diagramm anzuzeigen.")
else:
    if chart_type == "Kuchendiagramm":
        def autopct_format(pct):
            return ('%1.1f%%' % pct) if pct > 0 else ''  # Keine Anzeige bei 0%
        wedges, texts, autotexts = ax.pie(values, labels=categories.keys(), colors=[color]*len(values), autopct=autopct_format)
        for autotext in autotexts:
            autotext.set_color('black')
    elif chart_type == "Säulendiagramm":
        bars = ax.bar(categories.keys(), values, color=color)
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:.2f}', ha='center', va='bottom')
    elif chart_type == "MindMap":
        total_sum = sum(values)
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.axis('off')
        ax.add_patch(plt.Circle((0, 0), 0.3, color='lightgrey', ec='black'))
        ax.text(0, 0, f"{total_sum:.2f}\nBudget", ha='center', va='center', fontsize=12, color='black')
        angles = np.linspace(0, 2 * np.pi, len(values), endpoint=False)
        for i, (category, value) in enumerate(zip(categories.keys(), values)):
            x, y = np.cos(angles[i]), np.sin(angles[i])
            ax.add_patch(plt.Circle((x, y), 0.2 + 0.1 * (value / max(values)), color=color, alpha=0.6))
            ax.text(x, y, f"{category}\n{value:.2f}", ha='center', va='center', fontsize=10, color='black')
    
    # Diagramm anzeigen
    st.pyplot(fig)
