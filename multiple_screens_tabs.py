import os
import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# ------------------------
# Load Data for Both Screens
# ------------------------

# Dummy data for Screen 1 (replace with your own)
tickers_data = pd.DataFrame([
    {'SEHK Code': '0001', 'Open Interest': 120000, 'Skew': 0.45, 'Identifier': 'CKH', 'Notional traded': 5000000},
    {'SEHK Code': '0005', 'Open Interest': 95000, 'Skew': -0.12, 'Identifier': 'HSBC', 'Notional traded': 3200000},
    {'SEHK Code': '0700', 'Open Interest': 250000, 'Skew': 0.63, 'Identifier': 'TENCENT', 'Notional traded': 8000000},
    {'SEHK Code': '2318', 'Open Interest': 170000, 'Skew': 0.21, 'Identifier': 'PING AN', 'Notional traded': 4200000},
])
upside_data = pd.DataFrame([
    {'SEHK Code': '0700', 'Signal': 'Strong', 'Score': 9.1},
    {'SEHK Code': '0001', 'Signal': 'Moderate', 'Score': 7.5},
])
downside_data = pd.DataFrame([
    {'SEHK Code': '0005', 'Signal': 'Weak', 'Score': 3.2},
    {'SEHK Code': '2318', 'Signal': 'Moderate', 'Score': 5.0},
])

# Real data for Screen 2
df2 = pd.read_pickle('processed_data.pkl')
tickers2 = df2.columns.get_level_values('ticker').unique()
default_tickers2 = tickers2[:10]

# ------------------------
# App and Layout
# ------------------------

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# --- Helper Layouts ---

def big_table(df):
    return dash_table.DataTable(
        id='tickers-table',
        columns=[{"name": col, "id": col} for col in df.columns] +
                [{"name": "Column X", "id": "col_x"}, {"name": "Column Y", "id": "col_y"}],  # Placeholder columns
        data=df.to_dict('records'),
        style_table={'overflowX': 'auto', 'width': '100%'},
        style_header={'backgroundColor': '#222', 'color': '#fff', 'fontWeight': 'bold', 'fontSize': 16},
        style_cell={
            'backgroundColor': '#282828', 'color': '#fff', 'fontSize': 14,
            'padding': '8px', 'border': '1px solid #333'
        },
        page_size=12,
    )

def half_table(df, id):
    return dash_table.DataTable(
        id=id,
        columns=[{"name": col, "id": col} for col in df.columns],
        data=df.to_dict('records'),
        style_table={'overflowX': 'auto', 'width': '100%'},
        style_header={'backgroundColor': '#23272b', 'color': '#fff', 'fontWeight': 'bold', 'fontSize': 14},
        style_cell={'backgroundColor': '#282828', 'color': '#fff', 'fontSize': 13, 'padding': '6px', 'border': '1px solid #444'},
        page_size=5,
    )

# ----- SCREEN 2 LAYOUT -----
def screen2_layout():
    return dbc.Container([
        html.H1("Stock Metrics Dashboard", className="text-white mb-4"),
        html.Label("Select Metric:", className="text-info"),
        dcc.Dropdown(
            id='metric-dropdown',
            options=[
                {'label': 'Spot Price', 'value': 'spot_price'},
                {'label': 'Volume', 'value': 'volume'},
                {'label': 'Notional', 'value': 'notional'},
                {'label': 'Open Interest', 'value': 'open_interest'}
            ],
            value='spot_price',
            style={'width': '50%'}
        ),
        html.H2("Default Tickers", className="text-white mt-4 mb-3"),
        html.Div(
            [dcc.Graph(id=f'ticker-graph-{ticker}') for ticker in default_tickers2],
            style={'display': 'grid', 'gridTemplateColumns': 'repeat(2, 1fr)', 'gap': '20px'}
        ),
        html.H2("Search for a Ticker", className="text-white mt-4"),
        dbc.Row([
            dbc.Col(dcc.Input(id='ticker-search', type='text', placeholder='Enter ticker (e.g., ABC)', style={'width': '100%'}), width=6),
            dbc.Col(html.Button('Search', id='search-button', n_clicks=0, className="btn btn-info"), width=2),
        ], class_name="mb-2"),
        html.Div(id='search-result', className="text-info mb-2"),
        dcc.Graph(id='search-graph')
    ], fluid=True)

# ----- MAIN APP LAYOUT -----
app.layout = dbc.Container([
    html.Br(),
    dbc.Tabs([
        dbc.Tab(label="Summary Monitor", tab_id="summary", label_style={"fontWeight": "bold", "fontSize": 18}),
        dbc.Tab(label="Stock Metrics Dashboard", tab_id="metrics", label_style={"fontWeight": "bold", "fontSize": 18}),
        dbc.Tab(label="Screen 3", tab_id="screen3", label_style={"fontWeight": "bold", "fontSize": 18}),
    ], id="tabs", active_tab="summary", class_name="mb-4"),
    html.Div(id="tab-content"),
], fluid=True)

# ------------------------
# Tab Content Callback
# ------------------------
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab"),
)
def render_tab_content(active_tab):
    if active_tab == "summary":
        return dbc.Container([
            html.H2("Summary Monitor", className="text-white mb-4"),
            html.H4("Tickers of Interest", className="text-info mb-2"),
            big_table(tickers_data),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.H5("Upside Indicator", className="text-success mb-2"),
                    half_table(upside_data, 'upside-table')
                ], width=6),
                dbc.Col([
                    html.H5("Downside Indicator", className="text-danger mb-2"),
                    half_table(downside_data, 'downside-table')
                ], width=6),
            ], class_name="mb-4"),
            html.Div([
                dbc.Input(id='search-input', placeholder='Search by SEHK Code...', type='text', class_name="mb-3", style={"maxWidth": "300px"}),
            ]),
        ], fluid=True)
    elif active_tab == "metrics":
        return screen2_layout()
    else:
        # Placeholder for Screen 3
        return html.Div([
            html.H2("Screen 3", className="text-white"),
            html.P("Content coming soon.", className="text-secondary"),
        ])

# ------------------------
# Callbacks for Screen 2 (metrics)
# ------------------------

# Update graphs for default tickers
@app.callback(
    [Output(f'ticker-graph-{ticker}', 'figure') for ticker in default_tickers2],
    Input('metric-dropdown', 'value'),
    prevent_initial_call=False
)
def update_default_graphs(selected_metric):
    figures = []
    for ticker in default_tickers2:
        try:
            data = df2[(ticker, selected_metric)].reset_index()
            data.columns = ['date', selected_metric]
            fig = px.line(
                data, x='date', y=selected_metric,
                title=f'{ticker} - {selected_metric.replace("_", " ").title()}',
                labels={'date': 'Date', selected_metric: selected_metric.replace("_", " ").title()}
            )
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title=selected_metric.replace("_", " ").title(),
                template="plotly_dark"
            )
        except Exception as e:
            fig = px.line()
            fig.add_annotation(text=f"No data for {ticker}", xref="paper", yref="paper", showarrow=False)
        figures.append(fig)
    return figures

# Search for ticker and update graph
@app.callback(
    Output('search-graph', 'figure'),
    Output('search-result', 'children'),
    Input('search-button', 'n_clicks'),
    State('ticker-search', 'value'),
    State('metric-dropdown', 'value'),
    prevent_initial_call=True
)
def update_search_graph(n_clicks, search_ticker, selected_metric):
    if not search_ticker:
        return px.line(), "Enter a ticker and click Search."
    search_ticker = search_ticker.upper().strip()
    if search_ticker not in tickers2:
        return px.line(), f"Ticker {search_ticker} not found."
    data = df2[(search_ticker, selected_metric)].reset_index()
    data.columns = ['date', selected_metric]
    fig = px.line(
        data, x='date', y=selected_metric,
        title=f'{search_ticker} - {selected_metric.replace("_", " ").title()}',
        labels={'date': 'Date', selected_metric: selected_metric.replace("_", " ").title()}
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title=selected_metric.replace("_", " ").title(),
        template="plotly_dark"
    )
    return fig, f"Displaying data for {search_ticker}."

if __name__ == '__main__':
    app.run_server(debug=True)
