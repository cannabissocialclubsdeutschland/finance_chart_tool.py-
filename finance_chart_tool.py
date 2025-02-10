import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Farben für die Diagrammsegmente
colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]

# Streamlit-Seiteneinstellungen
st.set_page_config(page_title="Finanzberater-Tool", layout="wide")
st.title("Finanzberater-Tool")

# Funktion zur Berechnung der Summe aus Unterkategorien
def sum_categories(categories):
    return sum(categories.values())

# Eingabefelder für das Gesamtbudget und Unterkategorien
total_budget = st.sidebar.number_input("Gesamtbudget", min_value=0.0, value=0.0, step=0.1)
st.sidebar.header("Eingabewerte")

# Kategorien und Unterkategorien
categories = {
    "Fixkosten": {"Lebenshaltung": 0.0, "Miete": 0.0, "Versicherungen": 0.0, "Kommunikation": 0.0},
    "Freizeit": {"Urlaub": 0.0, "Hobbies": 0.0, "Anschaffungen": 0.0, "Spaß": 0.0},
    "Rücklagen": {"Riesterrente": 0.0, "Depots": 0.0, "Crypto": 0.0},
    "Sicherheit": {"Notfälle": 0.0, "Unerwartetes": 0.0}
}

values = []
for category, subcategories in categories.items():
    st.sidebar.subheader(category)
    for subcategory in subcategories:
        categories[category][subcategory] = st.sidebar.number_input(f"{subcategory}", min_value=0.0, value=0.0, step=0.1)
    values.append(sum_categories(subcategories))

# Auswahl des Diagrammtyps
chart_type = st.sidebar.selectbox("Diagrammtyp", ["Kuchendiagramm", "Säulendiagramm", "MindMap"])

# Diagramm erstellen
fig, ax = plt.subplots(figsize=(7, 4))  # Größe reduziert, um weniger Scrollen zu erfordern
if sum(values) == 0:
    st.warning("Bitte geben Sie mindestens einen positiven Wert ein, um das Diagramm anzuzeigen.")
else:
    if chart_type == "Kuchendiagramm":
        def autopct_format(pct):
            return ('%1.1f%%' % pct) if pct > 0 else ''  # Keine Anzeige bei 0%
        ax.pie(values, labels=categories.keys(), colors=colors, autopct=autopct_format)
    elif chart_type == "Säulendiagramm":
        ax.bar(categories.keys(), values, color=colors)
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
            ax.add_patch(plt.Circle((x, y), 0.2 + 0.1 * (value / max(values)), color=colors[i], alpha=0.6))
            ax.text(x, y, f"{category}\n{value:.2f}", ha='center', va='center', fontsize=10, color='black')
    
    # Diagramm anzeigen
    st.pyplot(fig)

# Berechnung der Differenz zwischen Gesamtbudget und Gesamtausgaben
remaining_budget = total_budget - sum(values)
box_color = "#d4edda" if remaining_budget >= 0 else "#f8d7da"

# Anzeige der verbleibenden Mittel
st.markdown(f"<div style='padding: 10px; background-color: {box_color}; border-radius: 5px;'>\n"
            f"<strong>Verbleibendes Budget:</strong> {remaining_budget:.2f} €\n"
            f"</div>", unsafe_allow_html=True)
