import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html

# Load your CSV
file_path = r'https://github.com/Nadunimithya/Lake_Tana/blob/main/Lake_tana.py'
df = pd.read_csv(file_path)

# Ensure 'Value' is numeric
df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

# Color mapping
color_map = {
    "Gross Inflow": "#606060",
    "Net Inflow": "#D98D8E",
    "P": "#B4B4B4",
    "DS": "#19a337",
    "Landscape ET": "#497E7C",
    "Exploitable Water": "#46B1E1",
    "Rainfall ET": "#A3DB76",
    "Incremental ET": "#0B76A0",
    "Available Water": "#0B76A0",
    "Non-Utilizable Flow": "#0B76A0",
    "Reserved Flow": "#0B76A0",
    "Managed Water": "#96DCF8",
    "Utilizable Water": "#96DCF8",
    "Non-Recoverable Flow": "#C1E5F5",
    "Incremental ET (Managed)": "#C1E5F5"
}

# Explanations
explanation_map = {
    "Gross Inflow": "Total water entering the basin from all sources.",
    "Net Inflow": "Water entering the basin after accounting for losses.",
    "P": "Precipitation: Rainfall received by the basin.",
    "DS": "Change in Storage: Change in water storage in the basin over time.",
    "Landscape ET": "Evapotranspiration from the landscape (natural vegetation).",
    "Exploitable Water": "Maximum water available for use.",
    "Rainfall ET": "Evapotranspiration directly related to rainfall.",
    "Incremental ET": "Evapotranspiration due to sources other than rainfall.",
    "Available Water": "Water that can be accessed for use in the basin.",
    "Non-Utilizable Flow": "Flow that cannot be used for practical purposes.",
    "Reserved Flow": "Water flow reserved for specific uses.",
    "Managed Water": "Water that is actively managed for use.",
    "Utilizable Water": "Water that can be used for new water resources development projects.",
    "Non-Recoverable Flow": "Water flow that cannot be recovered or reused.",
    "Incremental ET (Managed)": "Evapotranspiration related to managed land or resources."
}

# Create sunburst chart
def create_sunburst():
    labels = df['Label'].tolist()
    parents = df['Parent'].tolist()
    values = df['Value'].tolist()
    colors = [color_map.get(label, "#f1b04c") for label in labels]

    custom_data = [
        explanation_map.get(label, "No description") for label in labels
    ]
    hover_value = [
        -1 if label == "DS" else val for label, val in zip(labels, values)
    ]

    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
        marker=dict(colors=colors),
        insidetextfont=dict(size=24, family="Arial", color="black"),
        textinfo="label",
        insidetextorientation='auto',
        customdata=list(zip(hover_value, custom_data)),
        hovertemplate="<b>%{label}</b><br>Value: %{customdata[0]:.2f} km³/yr<br>Percentage: %{percentParent:.1%}<br>%{customdata[1]}<extra></extra>"
    ))

    fig.update_layout(
    margin=dict(t=0, l=0, r=0, b=0),  # Remove margins
    hoverlabel=dict(
        font_size=32,
        font_family="Arial, sans-serif"
    ),
    uniformtext=dict(
        # minsize=20,  # Minimum label font size
        # mode='show'  # Always show label even if it doesn't fit perfectly
    ),
    annotations=[dict(
        text="Lake Tana",  # Root label at center
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(
            size=30,
            color="black",
            family="Arial"
        ),
        xanchor="center",
        yanchor="middle"
    )]
)


    return fig

# Initialize Dash app
app = Dash(__name__)
app.title = "Lake Tana Water Flow"
server = app.server 

# App layout optimized for space
app.layout = html.Div([
    html.H1(
    "Lake Tana Water Flow (2010-2020) (km³/year)",
    style={
        'textAlign': 'center',
        'marginTop': '0px',
        'marginBottom': '0px',
        'fontSize': '32px',
        'fontWeight': 'bold',
        'lineHeight': '1.5'  # Tight line spacing
    }
),


    dcc.Graph(
        id='sunburst-chart',
        figure=create_sunburst(),
        style={
            'height': '93vh',
            'width': '100%',
            'margin': '0 auto',
            'padding': '0'
        }
    ),

    html.Div(
        "Outflow = Utilizable Water + Non-Utilizable Water + Reserved Flow + Non-Recoverable Flow",
        style={
            'textAlign': 'center',
            'marginTop': '0px',
            'fontSize': '28px',
            'fontStyle': 'italic'
        }
    )
])


if __name__ == '__main__':
    app.run(debug=True)
