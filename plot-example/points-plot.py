from fpl import FplCurrent,FplHistory
import numpy as np
import plotly.graph_objects as go

team = FplCurrent(7612489)

hisory = FplHistory(team.managerID, 1)


weeks_played = hisory.gameWeeks_played
gameweeks = np.arange(1, weeks_played + 1)
points = np.concatenate(
    np.array(
        [[FplHistory(team.managerID, n).points] for n in range(1, weeks_played + 1)]
    )
)

hover_text = [
    f"Gameweek {gameweek}<br>{point} points"
    for gameweek, point in zip(gameweeks, points)
]

fig = go.Figure(
    data=go.Bar(x=gameweeks, y=points, hovertext=hover_text, hoverinfo="text")
)

fig.update_layout(
    title={
        "text": "Points per Gameweek Plot",
        "x": 0.5,
        "xanchor": "center",
        "font": {
            "family": "Arial, sans-serif",
            "size": 24,
        },
    },
    xaxis_title={
        "text" : "Gameweek",
        "font": {
            "family": "Arial, sans-serif",
            "size": 18
        },
    },
    yaxis_title={
        "text" : "Points",
        "font": {
            "family": "Arial, sans-serif",
            "size": 18
        },
    },
    
    template = "plotly_dark"
)
fig.show()
