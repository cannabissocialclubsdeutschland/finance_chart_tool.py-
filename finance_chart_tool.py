import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Blautöne mit leichtem Kontrast
blue_shades = ["#A6CEE3", "#7EA8C4", "#5683A5", "#2E5E86"]
gold_line = "#FFD700"  # Goldene Linien

# Streamlit-Seiteneinstellungen
st.set_page_config(page_title="Finanzberater-Tool", layout="centered")

# Titel in einer Zeile (25% kleiner)
st.markdown("<h1 style='text-align: center; color: gold; font-size: 1.75rem;'>Finanzberater-Tool</h1>", unsafe_allow_html=True)

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

# Abstand zwischen Titel und Diagramm (nur für Desktop)
st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

# Diagramm erstellen
if sum(values) == 0:
    st.warning("Bitte geben Sie mindestens einen positiven Wert ein, um das Diagramm anzuzeigen.")
else:
    if chart_type == "Kuchendiagramm":
        fig, ax = plt.subplots(figsize=(7, 4))  # Kreis 15% größer
        def autopct_format(pct):
            return ('%1.1f%%' % pct) if pct > 0 else ''  # Keine Anzeige bei 0%
        wedges, texts, autotexts = ax.pie(
            values, labels=categories.keys(), colors=blue_shades, autopct=autopct_format,
            wedgeprops={'linewidth': 0.8, 'edgecolor': gold_line}  # Konturen 20% dünner
        )
        # Schriftgröße um 30% verkleinern
        for text in texts:
            text.set_fontsize(10)  # Standard ist ~14, daher 10 für ~30% kleiner
        for autotext in autotexts:
            autotext.set_fontsize(10)
            autotext.set_color('black')
    elif chart_type == "Säulendiagramm":
        fig, ax = plt.subplots(figsize=(8, 5))  # 20% größer
        bars = ax.bar(categories.keys(), values, color=blue_shades)
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:.2f}', ha='center', va='bottom', fontsize=10)
        # Obere und rechte Achsenlinie entfernen
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    elif chart_type == "MindMap":
        fig, ax = plt.subplots(figsize=(8, 8))  # Größeres Diagramm für MindMap
        total_sum = sum(values)
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.axis('off')

        # Hauptkreis in der Mitte
        ax.add_patch(plt.Circle((0, 0), 0.3, color='lightgrey', ec='black'))
        ax.text(0, 0, f"{total_sum:.2f}\nBudget", ha='center', va='center', fontsize=12, color='black')

        # Winkel für die Hauptpunkte
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False)

        # Hauptpunkte zeichnen
        for i, (category, subcategories) in enumerate(categories.items()):
            x, y = np.cos(angles[i]) * 1.2, np.sin(angles[i]) * 1.2  # Position der Hauptpunkte
            ax.add_patch(plt.Circle((x, y), 0.2, color=blue_shades[i], alpha=0.6))
            ax.text(x, y, f"{category}\n{sum(subcategories.values()):.2f}", ha='center', va='center', fontsize=10, color='black')

            # Unterpunkte zeichnen
            sub_angles = np.linspace(angles[i] - np.pi/6, angles[i] + np.pi/6, len(subcategories), endpoint=False)
            for j, (subcategory, value) in enumerate(subcategories.items()):
                sub_x, sub_y = np.cos(sub_angles[j]) * 1.8, np.sin(sub_angles[j]) * 1.8  # Position der Unterpunkte
                circle_size = 0.1 + 0.1 * (value / total_sum)  # Größe basierend auf dem Verhältnis zum Gesamtbudget
                ax.add_patch(plt.Circle((sub_x, sub_y), circle_size, color=blue_shades[i], alpha=0.6))
                ax.text(sub_x, sub_y, f"{subcategory}\n{value:.2f}", ha='center', va='center', fontsize=8, color='black')
                # Linie zwischen Haupt- und Unterpunkt
                ax.plot([x, sub_x], [y, sub_y], color=blue_shades[i], linewidth=0.5)

    # Diagramm anzeigen
    st.pyplot(fig)
