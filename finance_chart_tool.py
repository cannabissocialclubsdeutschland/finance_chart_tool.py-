import streamlit as st
import matplotlib.pyplot as plt

# Farben für die Diagrammsegmente
colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]

# Streamlit-Seiteneinstellungen
st.set_page_config(page_title="Finanzberater-Tool", layout="wide")
st.title("Finanzberater-Tool")

# Eingabefelder für die Zahlen
st.sidebar.header("Eingabewerte")
values = []
for i in range(1, 5):
    value = st.sidebar.number_input(f"Wert {i}", min_value=0.0, value=0.0, step=0.1)
    values.append(value)

# Auswahl des Diagrammtyps
chart_type = st.sidebar.selectbox("Diagrammtyp", ["Kuchendiagramm", "Säulendiagramm", "MindMap"])

# Diagramm erstellen
fig, ax = plt.subplots(figsize=(10, 6))
if chart_type == "Kuchendiagramm":
    ax.pie(values, labels=["Segment 1", "Segment 2", "Segment 3", "Segment 4"], colors=colors, autopct='%1.1f%%')
elif chart_type == "Säulendiagramm":
    ax.bar(["Segment 1", "Segment 2", "Segment 3", "Segment 4"], values, color=colors)
elif chart_type == "MindMap":
    ax.text(0.5, 0.5, f"MindMap-ähnliche Darstellung\n(Werte: {values[0]}, {values[1]}, {values[2]}, {values[3]})", 
            ha='center', va='center', fontsize=14, color='black')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

# Diagramm anzeigen
st.pyplot(fig)
