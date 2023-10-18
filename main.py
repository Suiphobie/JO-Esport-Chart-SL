import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Chargement des données
@st.cache
def load_data():
    return pd.read_csv("E-SPORT ET JO - Sheet1.csv")

data = load_data()

# Fonction pour créer un graphique en camembert
def plot_pie_chart(column_name, title):
    counts = data[column_name].value_counts()
    plt.figure(figsize=(8,6))
    plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    plt.title(title)
    return plt

# Titre de l'application
st.title("Résultats du sondage sur l'e-sport et les J.O.")

# Affichage des graphiques
st.pyplot(plot_pie_chart("À quelle tranche d'âge appartenez-vous ? ", "Répartition par tranche d'âge"))
st.pyplot(plot_pie_chart("As-tu entendu parler de la semaine \"The Olympic Esports Series 2023\" ?", "Connaissance de 'The Olympic Esports Series 2023'"))
