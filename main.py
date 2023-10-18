import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")


# Chargement des données
@st.cache
def load_data():
    return pd.read_csv("E-SPORT ET JO - Sheet1.csv")

data = load_data()

# Pie Chart Tranche Age
def adjusted_interactive_pie_chart(column_name, title):
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
    ).configure_view(
        strokeWidth=0
    ).configure_scale(
        bandPaddingInner=0.05
    )
    
    # Adjusting the margin
    chart = chart.configure_view(strokeWidth=0).configure_scale(bandPaddingInner=0.05).configure_mark(opacity=0.7).properties(
        width=350,
        height=300
    )
    
    return chart





# 1. Répartition par tranche d'âge
def age_distribution_chart():
    counts = data["À quelle tranche d'âge appartenez-vous ? "].value_counts().reset_index()
    counts.columns = ['Age Group', 'Count']
    chart = alt.Chart(counts).mark_bar().encode(
        x='Age Group:O',
        y='Count:Q',
        color='Age Group:N',
        tooltip=['Age Group', 'Count']
    ).properties(
        title="Répartition par tranche d'âge",
        width=400
    )
    return chart

# 2. Connaissance de 'The Olympic Esports Series 2023'
def knowledge_about_event_chart():
    counts = data["As-tu entendu parler de la semaine \"The Olympic Esports Series 2023\" ?"].value_counts().reset_index()
    counts.columns = ['Knowledge', 'Count']
    chart = alt.Chart(counts).mark_bar().encode(
        x='Knowledge:O',
        y='Count:Q',
        color='Knowledge:N',
        tooltip=['Knowledge', 'Count']
    ).properties(
        title="Connaissance de 'The Olympic Esports Series 2023'",
        width=300
    )
    return chart

# 3. Jeux les plus connus
def most_known_games_chart():
    # Extract game-related columns
    game_cols = [col for col in data.columns if "Parmi ces jeux lesquels connais-tu?" in col and "Aucun" not in col]
    counts = data[game_cols].sum().reset_index()
    counts.columns = ['Game', 'Count']
    counts['Game'] = counts['Game'].str.replace("Parmi ces jeux lesquels connais-tu? \(", "").str.replace("\)", "")
    chart = alt.Chart(counts).mark_bar().encode(
        x=alt.X('Game:O', sort='-y'),
        y='Count:Q',
        color='Game:N',
        tooltip=['Game', 'Count']
    ).properties(
        title="Jeux les plus connus",
        width=600
    )
    return chart


# Adjust the function to handle mixed data types
def adjusted_interactive_bar_chart(question_prefix, title):
    # Extract related columns
    related_cols = [col for col in data.columns if question_prefix in col and "Aucun" not in col]
    
    # Ensure the columns are numeric
    numeric_data = data[related_cols].apply(pd.to_numeric, errors='coerce')
    
    # Aggregate the data
    counts = numeric_data.sum().reset_index()
    counts.columns = ['Category', 'Count']
    
    # Clean category names
    counts['Category'] = counts['Category'].str.replace(question_prefix + " \(", "", regex=True).str.replace("\)", "", regex=True)
    
    # Create the chart
    chart = alt.Chart(counts).mark_bar().encode(
        x=alt.X('Category:O', sort='-y', title=''),
        y='Count:Q',
        color='Category:N',
        tooltip=['Category', 'Count']
    ).properties(
        title=title,
        width=600,  # Fixed width
        height=400
    )
    
    return chart




# Titre de l'application
st.title("Résultats du sondage sur l'e-sport et les J.O.")

# Utilisation de colonnes pour organiser les graphiques en colonnes
col1, col2, col3 = st.columns(3)  

# Affichage des graphiques dans les colonnes appropriées
with col1:
    st.altair_chart(adjusted_interactive_pie_chart("As-tu entendu parler de la semaine \"The Olympic Esports Series 2023\" ?", "Connaissance de 'The Olympic Esports Series 2023'"))
with col2:
    st.altair_chart(age_distribution_chart())
with col3:
    st.altair_chart(knowledge_about_event_chart())

# Pour le dernier graphique, car il est plus large, nous le plaçons en dehors des colonnes pour qu'il prenne toute la largeur de la page.
st.altair_chart(most_known_games_chart())

# Nouveaux graphiques interactifs
st.altair_chart(adjusted_interactive_bar_chart("Quelles sont les épreuves que tu connais ?", "Épreuves connues par les répondants"))
st.altair_chart(adjusted_interactive_bar_chart("Parmi ces jeux lesquels as-tu déjà joué?", "Jeux joués par les répondants"))
st.altair_chart(adjusted_interactive_bar_chart("Parmi ces athlètes, lesquels connais-tu ?", "Athlètes connus par les répondants"))

