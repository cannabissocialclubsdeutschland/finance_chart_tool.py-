import streamlit as st
import matplotlib.pyplot as plt

# Farben für die Diagrammsegmente
colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]

# Streamlit-Seiteneinstellungen
st.set_page_config(page_title="Finanzberater-Tool", layout="wide")
st.title("Finanzberater-Tool")

# Eingabefelder für die Zahlen und zugehörige Labels
labels = ["Fixkosten", "Freizeit", "Rücklagen", "Sicherheit"]
values = []

st.sidebar.header("Eingabewerte")
for label in labels:
    value = st.sidebar.number_input(label, min_value=0.0, value=0.0, step=0.1)
    values.append(value)

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
        ax.pie(values, labels=labels, colors=colors, autopct=autopct_format)
    elif chart_type == "Säulendiagramm":
        ax.bar(labels, values, color=colors)
    elif chart_type == "MindMap":
        ax.text(0.5, 0.5, f"MindMap-ähnliche Darstellung\n(Werte: {values[0]}, {values[1]}, {values[2]}, {values[3]})", 
                ha='center', va='center', fontsize=14, color='black')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
    
    # Diagramm anzeigen
    st.pyplot(fig)
