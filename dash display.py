import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load the DataFrame (assumes it's saved as a pickle file after running process_stock_data)
# Replace 'processed_data.pkl' with the path to your processed DataFrame
df = pd.read_pickle('processed_data.pkl')

# Get list of unique tickers
tickers = df.columns.get_level_values('ticker').unique()

# Select 10 tickers for default display (or fewer if <10 tickers exist)
default_tickers = tickers[:10]

# Initialize Dash app
app = dash.Dash(__name__)

# Layout of the Dash app
app.layout = html.Div([
    html.H1("Stock Metrics Dashboard"),
    
    # Dropdown for selecting metric to display
    html.Label("Select Metric:"),
    dcc.Dropdown(
        id='metric-dropdown',
        options=[
            {'label': 'Spot Price', 'value': 'spot_price'},
            {'label': 'Volume', 'value': 'volume'},
            {'label': 'Notional', 'value': 'notional'},
            {'label': 'Open Interest', 'value': 'open_interest'}
        ],
        value='spot_price',  # Default metric
        style={'width': '50%'}
    ),
    
    # Graphs for 10 default tickers
    html.H2("Default Tickers"),
    html.Div([
        dcc.Graph(id=f'ticker-graph-{ticker}') for ticker in default_tickers
    ], style={'display': 'grid', 'grid-template-columns': 'repeat(2, 1fr)', 'gap': '20px'}),
    
    # Search functionality
    html.H2("Search for a Ticker"),
    dcc.Input(id='ticker-search', type='text', placeholder='Enter ticker (e.g., ABC)', style={'width': '50%'}),
    html.Button('Search', id='search-button', n_clicks=0),
    html.Div(id='search-result'),
    dcc.Graph(id='search-graph')
])

# Callback to update default ticker graphs
@app.callback(
    [Output(f'ticker-graph-{ticker}', 'figure') for ticker in default_tickers],
    [Input('metric-dropdown', 'value')]
)
def update_default_graphs(selected_metric):
    figures = []
    for ticker in default_tickers:
        # Extract data for the specific ticker and metric
        data = df[(ticker, selected_metric)].reset_index()
        data.columns = ['date', selected_metric]
        
        # Create line plot
        fig = px.line(
            data,
            x='date',
            y=selected_metric,
            title=f'{ticker} - {selected_metric.replace("_", " ").title()}',
            labels={'date': 'Date', selected_metric: selected_metric.replace("_", " ").title()}
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title=selected_metric.replace("_", " ").title(),
            template="plotly_white"
        )
        figures.append(fig)
    return figures

# Callback to update search graph
@app.callback(
    [Output('search-graph', 'figure'), Output('search-result', 'children')],
    [Input('search-button', 'n_clicks')],
    [Input('ticker-search', 'value'), Input('metric-dropdown', 'value')]
)
def update_search_graph(n_clicks, search_ticker, selected_metric):
    if n_clicks == 0 or not search_ticker:
        return px.line(), "Enter a ticker and click Search."
    
    search_ticker = search_ticker.upper().strip()
    if search_ticker not in tickers:
        return px.line(), f"Ticker {search_ticker} not found."
    
    # Extract data for the searched ticker and metric
    data = df[(search_ticker, selected_metric)].reset_index()
    data.columns = ['date', selected_metric]
    
    # Create line plot
    fig = px.line(
        data,
        x='date',
        y=selected_metric,
        title=f'{search_ticker} - {selected_metric.replace("_", " ").title()}',
        labels={'date': 'Date', selected_metric: selected_metric.replace("_", " ").title()}
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title=selected_metric.replace("_", " ").title(),
        template="plotly_white"
    )
    
    return fig, f"Displaying data for {search_ticker}."

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
