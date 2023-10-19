import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")



# Chargement des données
@st.cache
def load_data():
    return pd.read_csv("E-SPORT ET JO - Sheet1.csv")

data = load_data()






# Afficher le nombre de répondants

st.title("Analyse détaillée en fonction de la tranche d'âge sélectionnée")

# 1. Répartition par tranche d'âge
def age_distribution_chart():
    counts = data["À quelle tranche d'âge appartenez-vous ? "].value_counts().sort_index().reset_index()
    counts.columns = ['Tranche Âge', 'Nombre']
    chart = alt.Chart(counts).mark_arc(innerRadius=50, outerRadius=150).encode(theta="Nombre:Q",
        color=alt.Color('Tranche Âge:N'),
        tooltip=['Tranche Âge', 'Nombre']).properties(
        title="Répartition par tranche d'âge de tous les répondants",
        width=600
        ).project(
        type='identity', scale=2
    )
    return chart

# Création de trois colonnes : gauche, centre, droite
left_column, center_column, right_column = st.columns(3)

# Affichage du graphique dans la colonne centrale
with left_column:
    st.write(f"Nombre de répondants: {len(data)}")
with center_column:
    st.altair_chart(age_distribution_chart())




# 2. Connaissance de 'The Olympic Esports Series 2023'
def knowledge_about_event_chart():
    counts = filtered_data["As-tu entendu parler de la semaine \"The Olympic Esports Series 2023\" ?"].value_counts().reset_index()
    counts.columns = ['Knowledge', 'Nombre']
    chart = alt.Chart(counts).mark_bar().encode(
        x='Knowledge:O',
        y='Nombre:Q',
        color='Knowledge:N',
        tooltip=['Knowledge', 'Nombre']
    ).properties(
        title="Connaissance de 'The Olympic Esports Series 2023'",
        width=300
    )
    return chart

# 3. Jeux les plus connus
def most_known_games_chart():
    # Extract game-related columns
    game_cols = [col for col in filtered_data.columns if "Parmi ces jeux lesquels connais-tu?" in col and "Aucun" not in col]
    counts = filtered_data[game_cols].sum().reset_index()
    counts.columns = ['Game', 'Nombre']
    counts['Game'] = counts['Game'].str.extract(r"\((.*?)\)", expand=False)
    chart = alt.Chart(counts).mark_bar().encode(
        x=alt.X('Game:O', sort='-y'),
        y='Nombre:Q',
        color='Game:N',
        tooltip=['Game', 'Nombre']
    ).properties(
        title="Jeux les plus connus",
        width=600
    )
    return chart


# Adjust the function to handle mixed data types
def adjusted_interactive_bar_chart(question_prefix, title):
    # Extract related columns
    related_cols = [col for col in filtered_data.columns if question_prefix in col and "Aucun" not in col]
    
    # Ensure the columns are numeric
    numeric_data = filtered_data[related_cols].apply(pd.to_numeric, errors='coerce')
    
    # Aggregate the data
    counts = numeric_data.sum().reset_index()
    counts.columns = ['Category', 'Nombre']
    
    # Clean category names
    counts['Category'] = counts['Category'].str.extract(r"\((.*?)\)", expand=False)
    
    # Create the chart
    chart = alt.Chart(counts).mark_bar().encode(
        x=alt.X('Category:O', sort='-y', title=''),
        y='Nombre:Q',
        color='Category:N',
        tooltip=['Category', 'Nombre']
    ).properties(
        title=title,
        width=600,  # Fixed width
        height=400
    )
    
    return chart




# Titre de l'application
st.title("Résultats du sondage sur l'e-sport et les J.O.")

# Création d'un widget pour la sélection de la tranche d'âge
age_selection = st.selectbox("Sélectionnez une tranche d'âge:", options=["Tous"] + list(data["À quelle tranche d'âge appartenez-vous ? "].unique()), index=0, key="age_selection_1")


# Filtrage des données en fonction de la tranche d'âge sélectionnée

filtered_data = data if age_selection == "Tous" else data[data["À quelle tranche d'âge appartenez-vous ? "] == age_selection]


# Utilisation de colonnes pour organiser les graphiques en colonnes
col1, col2 = st.columns(2)  

# Affichage des graphiques dans les colonnes appropriées

with col1:
    st.altair_chart(knowledge_about_event_chart())
with col2: 
    st.altair_chart(adjusted_interactive_bar_chart("Quelles sont les épreuves que tu connais ?", "Épreuves connues par les répondants"))
# Nouveaux graphiques interactifs
c1, c2 = st.columns(2)

with c1:
    st.altair_chart(adjusted_interactive_bar_chart("Parmi ces athlètes, lesquels connais-tu ?", "Athlètes connus par les répondants"))
with c2 : 
    st.altair_chart(most_known_games_chart())
    