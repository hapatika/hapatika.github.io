# Screen with tabs

import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

# Sample data (replace with your actual data)
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

# App initialization
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

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

app.layout = dbc.Container([
    html.Br(),
    dbc.Tabs([
        dbc.Tab(label="Summary Monitor", tab_id="summary", label_style={"fontWeight": "bold", "fontSize": 18}),
        dbc.Tab(label="Screen 2", tab_id="screen2", label_style={"fontWeight": "bold", "fontSize": 18}),
        dbc.Tab(label="Screen 3", tab_id="screen3", label_style={"fontWeight": "bold", "fontSize": 18}),
    ], id="tabs", active_tab="summary", class_name="mb-4"),
    html.Div(id="tab-content"),
], fluid=True)

@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"),
     Input('search-input', 'value')],  # For search
)
def render_tab_content(active_tab, search_value):
    if active_tab == "summary":
        # Filter table if search is used
        df = tickers_data
        if search_value:
            df = df[df['SEHK Code'].str.contains(search_value)]
        return dbc.Container([
            html.H2("Summary Monitor", className="text-white mb-4"),
            html.H4("Tickers of Interest", className="text-info mb-2"),
            big_table(df),
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
    else:
        # Placeholder content for other screens
        return html.Div([
            html.H2(f"Screen {active_tab[-1]}", className="text-white"),
            html.P("Content coming soon.", className="text-secondary"),
        ])

# To make sure search-input always exists in the layout for callback
@app.callback(
    Output('search-input', 'value'),
    Input('tabs', 'active_tab')
)
def reset_search(active_tab):
    return ''

if __name__ == '__main__':
    app.run_server(debug=True)
