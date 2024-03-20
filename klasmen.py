import streamlit as st
import requests
import pandas as pd

# Function untuk mengambil data Bundesliga dari API
def get_bundesliga_standings():
    url = "https://bundesliga-standings.p.rapidapi.com/"
    headers = {
        "X-RapidAPI-Key": "4ce38c9c05msh570b364bd182acep15631ajsn7cf38bd004ec",
        "X-RapidAPI-Host": "bundesliga-standings.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Function untuk mengambil data Serie A dari API
def get_serie_A_standings():
    url = "https://serie-a2.p.rapidapi.com/leaderboard"
    headers = {
        "X-RapidAPI-Key": "4ce38c9c05msh570b364bd182acep15631ajsn7cf38bd004ec",
        "X-RapidAPI-Host": "serie-a2.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Main function untuk memulai aplikasi
def main():
    st.markdown(
        "<style>"
        "body { background-color: #e7d5ab; font-family: 'Arial', sans-serif; }"
        "h1 { color: #1f1807; text-align: center; }"
        "table { font-family: 'Poppins', sans-serif; border-collapse: collapse; width: 100%; border-radius: 10px; overflow: hidden; }"
        ".bundesliga th { background-color: #7b000c; color: white; font-weight: bold; padding: 15px 10px 15px 10px; font-family: 'Arial', sans-serif;}"
        ".serie_A th { background-color: #000c7b; color: white; font-weight: bold; padding: 15px 10px 15px 10px; font-family: 'Arial', sans-serif;}"
        "th, td { border: 1px solid #dddddd; text-align: left; padding: 8px; }"
        "</style>",
        unsafe_allow_html=True
    )

    # Navigation bar untuk memilih liga
    league = st.sidebar.selectbox("Select League", ["Bundesliga", "Serie A"])

    if league == "Bundesliga":
        display_bundesliga_standings()
    elif league == "Serie A":
        display_serie_A_standings()

# Function untuk menampilkan klasemen Bundesliga dalam tabel
def display_bundesliga_standings():
    st.header("Bundesliga Standings")
    standings = get_bundesliga_standings()
    display_standings(standings, "bundesliga")  # Menambahkan class untuk styling

# Function untuk menampilkan klasemen Serie A dalam tabel
def display_serie_A_standings():
    st.header("Serie A Standings")
    standings = get_serie_A_standings()
    display_standings(standings, "serie_A")  # Menambahkan class untuk styling

# Function untuk menampilkan klasemen dalam tabel
def display_standings(standings, league_class):
    data = []
    for team_data in standings:
        team = team_data['team']
        stats = team_data['stats']
        # Menampilkan logo setiap tim
        team_logo = f'<img style="margin-right: 10px;" src="{team["logo"]}" width="30" height="30">'
        row = {
            'Rank': stats["rank"],
            'Team': f"<div style='display: flex; align-items: center; width: 100%;'>{team_logo} <span>{team['name']}</span></div>",
            'GP': stats["gamesPlayed"],
            'Wins': stats["wins"],
            'Draws': stats["ties"],
            'Losses': stats["losses"],
            'GF': stats["goalsFor"],
            'GA': stats["goalsAgainst"],
            'GD': stats["goalDifference"],
            'Points': stats["points"],
            'Abbreviation': team["abbreviation"]
        }
        data.append(row)

    df = pd.DataFrame(data)
    df_html = df.to_html(escape=False, index=False)
    # Menggunakan CSS untuk membuat tabel lebih kecil dan mengganti warna header sesuai dengan liga
    df_html = df_html.replace('<table', f'<table class="{league_class}" style="font-size: 12px;"')
    df_html = df_html.replace('<th>Team</th>', '<th style="text-align: center;">Team</th>')
    st.markdown(df_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
