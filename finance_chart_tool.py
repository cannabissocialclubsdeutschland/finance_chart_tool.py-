import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Farben
blue_shades = ["#A6CEE3", "#7EA8C4", "#5683A5", "#2E5E86"]  # Blautöne
gold_color = "#FFD700"  # Goldene Farbe für Budget-Kreis und Konturen
gold_line = gold_color  # Goldene Linien

# Streamlit-Seiteneinstellungen
st.set_page_config(page_title="Finanzberater-Tool", layout="centered")

# Titel in einer Zeile (25% kleiner)
st.markdown(f"<h1 style='text-align: center; color: {gold_color}; font-size: 1.75rem;'>Finanzberater-Tool</h1>", unsafe_allow_html=True)

# Sidebar-Header (dauerhaft sichtbar)
st.sidebar.markdown("<h1 style='font-family: Arial; font-weight: bold;'>United Hands Capital</h1>", unsafe_allow_html=True)

# Diagrammtyp-Auswahl direkt über dem Diagramm
chart_type = st.selectbox("Diagramm-Typ", ["Kuchendiagramm", "Säulendiagramm", "MindMap"], key="chart_type")

# Eingabefeld für das Gesamtbudget
total_budget = st.sidebar.number_input("Gesamtbudget", min_value=0.0, value=0.0, step=0.1)

# Kategorien und Unterkategorien
categories = {
    "Fixkosten": {"Lebenshaltung": 0.0, "Miete": 0.0, "Versicherungen": 0.0, "Kommunikation": 0.0},
    "Freizeit": {"Urlaub": 0.0, "Hobbies": 0.0, "Anschaffungen": 0.0, "Spaß": 0.0},
    "Rücklagen": {"Riesterrente": 0.0, "Depots": 0.0, "Crypto": 0.0},
    "Sicherheit": {"Notfälle": 0.0, "Unerwartetes": 0.0}
}

# Dropdown-Menüs für Kategorien mit klassischen Dropdowns
values = []
for category, subcategories in categories.items():
    with st.sidebar.expander(f"{category}"):
        for subcategory in subcategories:
            categories[category][subcategory] = st.number_input(
                f"{subcategory}", min_value=0.0, value=categories[category][subcategory], step=0.1, key=f"{category}_{subcategory}"
            )
    values.append(sum(subcategories.values()))

# Berechnung der Differenz zwischen Gesamtbudget und Gesamtausgaben
remaining_budget = total_budget - sum(values)
box_color = "#d4edda" if remaining_budget >= 0 else "#f8d7da"

# Anzeige der verbleibenden Mittel über dem Diagramm
st.markdown(f"<div style='padding: 10px; background-color: {box_color}; border-radius: 5px;'>\n"
            f"<strong>Verbleibendes Budget:</strong> {remaining_budget:.2f} €\n"
            f"</div>", unsafe_allow_html=True)

# Abstand zwischen Titel und Diagramm (nur für Desktop)
st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

# Diagramm erstellen
if sum(values) == 0:
    st.warning("Bitte geben Sie mindestens einen positiven Wert ein, um das Diagramm anzuzeigen.")
else:
    with st.container():
        fig, ax = plt.subplots(figsize=(15, 12))  # Größere Diagrammgröße
        if chart_type == "Kuchendiagramm":
            def autopct_format(pct):
                return ('%1.1f%%' % pct) if pct > 0 else ''
            wedges, texts, autotexts = ax.pie(
                values, labels=categories.keys(), colors=blue_shades, autopct=autopct_format,
                wedgeprops={'linewidth': 0.8, 'edgecolor': gold_line}
            )
            for text in texts:
                text.set_fontsize(8)
            for autotext in autotexts:
                autotext.set_fontsize(8)
                autotext.set_color('black')
        elif chart_type == "Säulendiagramm":
            bars = ax.bar(categories.keys(), values, color=blue_shades, edgecolor=gold_color, linewidth=0.72)
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:.2f}', ha='center', va='bottom', fontsize=10)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
        elif chart_type == "MindMap":
            total_sum = sum(values)
            ax.set_xlim(-2.5, 2.5)
            ax.set_ylim(-2.5, 2.5)
            ax.axis('off')

            ax.add_patch(plt.Circle((0, 0), 0.3, color=gold_color, ec='black'))
            ax.text(0, 0, f"{total_sum:.2f}\nBudget", ha='center', va='center', fontsize=10, color='black')

            angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False)

            for i, (category, subcategories) in enumerate(categories.items()):
                x, y = np.cos(angles[i]) * 0.8, np.sin(angles[i]) * 0.8  # Größerer Abstand
                ax.add_patch(plt.Circle((x, y), 0.2, color=blue_shades[i], alpha=0.6, zorder=3))
                ax.text(x, y, f"{category}\n{sum(subcategories.values()):.2f}", ha='center', va='center', fontsize=8, color='black', zorder=4)  # Kleinere Schriftgröße
                ax.plot([0.3 * np.cos(angles[i]), x - 0.2 * np.cos(angles[i])], 
                        [0.3 * np.sin(angles[i]), y - 0.2 * np.sin(angles[i])], 
                        color=blue_shades[i], linewidth=0.5, zorder=1)

                sub_angles = np.linspace(angles[i] - np.pi/8, angles[i] + np.pi/8, len(subcategories), endpoint=False)
                for j, (subcategory, value) in enumerate(subcategories.items()):
                    sub_x, sub_y = np.cos(sub_angles[j]) * 1.4, np.sin(sub_angles[j]) * 1.4  # Symmetrischere Anordnung
                    circle_size = 0.1 + 0.1 * (value / total_sum) if total_sum > 0 else 0.1
                    ax.add_patch(plt.Circle((sub_x, sub_y), circle_size, color=blue_shades[i], alpha=0.6, zorder=3))
                    ax.text(sub_x, sub_y, f"{value:.2f}", ha='center', va='center', fontsize=8, color='black', zorder=4)
                    ax.plot([x + 0.2 * np.cos(sub_angles[j]), sub_x - circle_size * np.cos(sub_angles[j])], 
                            [y + 0.2 * np.sin(sub_angles[j]), sub_y - circle_size * np.sin(sub_angles[j])], 
                            color=blue_shades[i], linewidth=0.5, zorder=1)

        st.pyplot(fig)
