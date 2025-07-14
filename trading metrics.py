import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output

# Initialize the Dash app with Bootstrap styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Read data from CSV file (replace 'trading_data.csv' with your file path)
# Example CSV structure: Ticker, Underlying_Name, OInt_Calls, OInt_Puts, Volume, Spot, Contract_Size, IV
try:
    df = pd.read_csv('trading_data.csv')
except FileNotFoundError:
    # Fallback: Create a sample DataFrame if file not found
    df = pd.DataFrame({
        'Ticker': ['AAPL', 'GOOGL', 'TSLA'],
        'Underlying_Name': ['Apple Inc.', 'Alphabet Inc.', 'Tesla Inc.'],
        'OInt_Calls': [1000, 1500, 2000],
        'OInt_Puts': [800, 1200, 1800],
        'Volume': [500, 700, 1000],
        'Spot': [150.25, 2800.50, 900.75],
        'Contract_Size': [100, 100, 100],
        'IV': [25.5, 22.3, 35.7]
    })

# Compute derived columns
df['Total_OInt'] = df['OInt_Calls'] + df['OInt_Puts']
df['Put_Call_Ratio'] = df.apply(lambda x: x['OInt_Puts'] / x['OInt_Calls'] if x['OInt_Calls'] != 0 else float('inf'), axis=1)
df['Total_Notional_Traded'] = df['Volume'] * df['Spot'] * df['Contract_Size']

# Format columns for display
df['IV'] = df['IV'].round(2)  # Round IV to 2 decimal places
df['Put_Call_Ratio'] = df['Put_Call_Ratio'].round(2)  # Round Put/Call Ratio to 2 decimal places
df['Total_Notional_Traded'] = df['Total_Notional_Traded'].round(2)  # Round Notional to 2 decimal places

# Define the app layout with navigation
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Front page layout
front_page_layout = dbc.Container(
    [
        html.H1(
            "Volatility Monitor and Trading Indicators",
            className="text-center my-5",
            style={"fontWeight": "bold", "color": "#2c3e50"},
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Link(
                        dbc.Button(
                            "Market Overview",
                            color="primary",
                            className="w-100 mb-3",
                            style={"fontSize": "1.2rem"},
                        ),
                        href="/page1",
                    ),
                    width=3,
                    className="d-flex justify-content-center",
                ),
                dbc.Col(
                    dcc.Link(
                        dbc.Button(
                            "Page 2",
                            color="primary",
                            className="w-100 mb-3",
                            style={"fontSize": "1.2rem"},
                        ),
                        href="/page2",
                    ),
                    width=3,
                    className="d-flex justify-content-center",
                ),
                dbc.Col(
                    dcc.Link(
                        dbc.Button(
                            "Page 3",
                            color="primary",
                            className="w-100 mb-3",
                            style={"fontSize": "1.2rem"},
                        ),
                        href="/page3",
                    ),
                    width=3,
                    className="d-flex justify-content-center",
                ),
                dbc.Col(
                    dcc.Link(
                        dbc.Button(
                            "Page 4",
                            color="primary",
                            className="w-100 mb-3",
                            style={"fontSize": "1.2rem"},
                        ),
                        href="/page4",
                    ),
                    width=3,
                    className="d-flex justify-content-center",
                ),
            ],
            justify="center",
        ),
    ],
    fluid=True,
    className="py-5",
)

# Page 1 layout (Market Overview Table)
page1_layout = dbc.Container(
    [
        html.H2("Market Overview", className="text-center my-4"),
        dcc.Link(
            dbc.Button("Back to Home", color="secondary", className="mb-3"),
            href="/",
        ),
        dash_table.DataTable(
            id='market-table',
            columns=[
                {'name': 'Ticker', 'id': 'Ticker'},
                {'name': 'Underlying Name', 'id': 'Underlying_Name'},
                {'name': 'OInt on Calls', 'id': 'OInt_Calls'},
                {'name': 'OInt on Puts', 'id': 'OInt_Puts'},
                {'name': 'Total OInt', 'id': 'Total_OInt'},
                {'name': 'Put Call Ratio', 'id': 'Put_Call_Ratio'},
                {'name': 'Total Notional Traded', 'id': 'Total_Notional_Traded'},
        {'name': 'IV (%)', 'id': 'IV'},
            ],
            data=df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_cell={
                'textAlign': 'center',
                'padding': '5px',
                'fontSize': '14px',
            },
            style_header={
                'backgroundColor': '#2c3e50',
                'color': 'white',
                'fontWeight': 'bold',
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f8f9fa',
                }
            ],
            page_size=10,
            sort_action='native',
            filter_action='native',
        ),
    ],
    fluid=True,
    className="py-5",
)

# Callback to handle page navigation
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/page1':
        return page1_layout
    else:
        return front_page_layout

if __name__ == '__main__':
    app.run(debug=True)