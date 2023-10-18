import streamlit as st
import pandas as pd
import altair as alt

# Chargement des données
@st.cache
def load_data():
    return pd.read_csv("E-SPORT ET JO - Sheet1.csv")

data = load_data()

# Fonction pour créer un graphique en camembert interactif avec Altair
def interactive_pie_chart(column_name, title):
    counts = data[column_name].value_counts().reset_index()
    counts.columns = ['Category', 'Count']

    chart = alt.Chart(counts).mark_arc(innerRadius=50, outerRadius=150).encode(
        theta='Count:Q',
        color='Category:N',
        tooltip=['Category', 'Count']
    ).properties(
        title=title,
        width=300,
        height=300
    )
    return chart

# Titre de l'application
st.title("Résultats du sondage sur l'e-sport et les J.O.")

# Affichage du graphique interactif
st.altair_chart(interactive_pie_chart("As-tu entendu parler de la semaine \"The Olympic Esports Series 2023\" ?", "Connaissance de 'The Olympic Esports Series 2023'"))
