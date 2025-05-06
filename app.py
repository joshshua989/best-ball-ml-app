import streamlit as st
import json
from load_stats import get_qb_projections_with_predictions

# Mock data for demonstration
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
qb_predictions = get_qb_projections_with_predictions()

# Merge predictions into available players
for player in draft_data['available_players']:
    match = qb_predictions[qb_predictions['name'].str.contains(player['name'], case=False)]
    if not match.empty:
        player['Predicted FPTS'] = match.iloc[0]['Predicted FPTS']
        player['High Performer'] = match.iloc[0]['High Performer']
    else:
        player['Predicted FPTS'] = None
        player['High Performer'] = "Unknown"

st.title("🤖 DRAFT VADER v1.1 🏈")

# Draft Pick Section
st.header("Make a Pick")
player_names = [p['name'] for p in draft_data['available_players']]
selected_player = st.selectbox("Select Player", player_names)
selected_team = st.selectbox("Select Team", [t['name'] for t in draft_data['teams']])

if st.button("Draft Player"):
    player = next(p for p in draft_data['available_players'] if p['name'] == selected_player)
    team = next(t for t in draft_data['teams'] if t['name'] == selected_team)
    team['roster'].append(player)
    draft_data['available_players'].remove(player)
    st.success(f"{player['name']} drafted to {team['name']}")

# Draft Board
st.header("🏈 Draft Board")
for team in draft_data['teams']:
    st.markdown(f"### {team['name']}")
    for player in team['roster']:
        highlight = "🟢" if player.get('High Performer') == "High" else "⚪️"
        st.markdown(
            f"- {highlight} **{player['name']}** ({player['position']}) — {player.get('Predicted FPTS', 'N/A')} pts"
        )

# Recommended Picks
st.header("🔥 Recommended QBs")
recommended_qbs = sorted(
    [p for p in draft_data['available_players'] if p['position'] == 'QB' and p.get('High Performer') == 'High'],
    key=lambda x: x.get('Predicted FPTS', 0),
    reverse=True
)[:5]

for p in recommended_qbs:
    st.markdown(f"- **{p['name']}** — {p['Predicted FPTS']:.2f} pts")