# app.py

# 🧩 Summary:
# You're building a Streamlit fantasy football draft app that:

#   Loads live QB projections.

#   Uses machine learning to predict performance.

#   Lets users draft players to teams.

#   Recommends high-value QBs based on the predictions.

# ---------------------- Libraries ----------------------
import streamlit as st
import json
from load_stats import get_qb_projections_with_predictions
# ---------------------- Libraries ----------------------


# ---------------------- Data Handling ----------------------
st.set_page_config(page_title="🏈 Best Ball MachLearn App v1.0 🤖")

# --- Mock data for demonstration ---
#   Initializes mock draft data - 
#       Checks if 'draft_data' exists in the Streamlit session.
#       If not, creates:
#           2 teams (Team A, Team B)
#           3 QBs (Josh Allen, Patrick Mahomes, Jalen Hurts) as available players.
if 'draft_data' not in st.session_state:
    st.session_state.draft_data = {
        'teams': [
            {'name': 'Team A', 'roster': []},
            {'name': 'Team B', 'roster': []}
        ],
        'available_players': [
            {'name': 'Josh Allen', 'position': 'QB'},
            {'name': 'Patrick Mahomes', 'position': 'QB'},
            {'name': 'Jalen Hurts', 'position': 'QB'}
        ]
    }

draft_data = st.session_state.draft_data

#   Loads QB projections with ML predictions from load_stats.py.
qb_predictions = get_qb_projections_with_predictions()

#   Merges fantasy projections and "High Performer" predictions into each available player using partial name matching.
for player in draft_data['available_players']:
    match = qb_predictions[qb_predictions['name'].str.contains(player['name'], case=False)]
    if not match.empty:
        player['Predicted FPTS'] = match.iloc[0]['Predicted FPTS']
        player['High Performer'] = match.iloc[0]['High Performer']
    else:
        player['Predicted FPTS'] = None
        player['High Performer'] = "Unknown"
# ---------------------- Data Handling ----------------------


# ---------------------- User Interface ----------------------
# Displays Streamlit app UI
st.title("🤖 DRAFT VADER v1.1 🏈")

# Draft Pick Section:
st.header("Make a Pick")
player_names = [p['name'] for p in draft_data['available_players']]
#   Lets user choose a player and a team from dropdowns.
selected_player = st.selectbox("Select Player", player_names)
selected_team = st.selectbox("Select Team", [t['name'] for t in draft_data['teams']])

#   On button click, assigns player to team and removes from available pool.
if st.button("Draft Player"):
    player = next(p for p in draft_data['available_players'] if p['name'] == selected_player)
    team = next(t for t in draft_data['teams'] if t['name'] == selected_team)
    team['roster'].append(player)
    draft_data['available_players'].remove(player)
    st.success(f"{player['name']} drafted to {team['name']}")

# Draft Board
st.header("🏈 Draft Board")
#   Displays each team's roster.
for team in draft_data['teams']:
    st.markdown(f"### {team['name']}")
    #   Uses 🟢 if a player is predicted as a high performer, ⚪️ otherwise.
    for player in team['roster']:
        highlight = "🟢" if player.get('High Performer') == "High" else "⚪️"
        st.markdown(
            f"- {highlight} **{player['name']}** ({player['position']}) — {player.get('Predicted FPTS', 'N/A')} pts"
        )

# Recommended Picks
st.header("🔥 Recommended QBs")
#   Shows top 5 available QBs with the highest predicted fantasy points who are also labeled as "High Performer".
recommended_qbs = sorted(
    [p for p in draft_data['available_players'] if p['position'] == 'QB' and p.get('High Performer') == 'High'],
    key=lambda x: x.get('Predicted FPTS', 0),
    reverse=True
)[:5]

for p in recommended_qbs:
    st.markdown(f"- **{p['name']}** — {p['Predicted FPTS']:.2f} pts")
# ---------------------- User Interface ----------------------