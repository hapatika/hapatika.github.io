import dash_ag_grid as dag
from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash_mantine_components as dmc
from dash_iconify import DashIconify

app = Dash(__name__)

# Your sample options data (replace with your real data)
option_data = {
    "AAPL": pd.DataFrame({
        "Date": pd.date_range("2024-06-01", periods=30, freq="D"),
        "Notional Traded": [1e8 + i*1e6 for i in range(30)],
        "Put OI": [2e6 + ((-1)**i)*5e4 for i in range(30)],
        "Call OI": [3e6 + ((-1)**(i+1))*6e4 for i in range(30)],
    }),
    "MSFT": pd.DataFrame({
        "Date": pd.date_range("2024-06-01", periods=30, freq="D"),
        "Notional Traded": [1e8 + i*1.2e6 for i in range(30)],
        "Put OI": [1.5e6 + ((-1)**i)*4e4 for i in range(30)],
        "Call OI": [2.5e6 + ((-1)**(i+1))*5e4 for i in range(30)],
    }),
    # add more tickers as needed
}

# Table data (replace with your real data)
table_data = [
    {
        "Ticker": "AAPL",
        "Price Action": "Up",
        "Change in Notional Traded": 0.05,
        "Skew": 0.15,
        "Comments": "Bullish OI build",
    },
    {
        "Ticker": "MSFT",
        "Price Action": "Flat",
        "Change in Notional Traded": -0.01,
        "Skew": -0.10,
        "Comments": "Steady flow",
    },
]

columnDefs = [
    {"headerName": "Ticker", "field": "Ticker"},
    {"headerName": "Price Action", "field": "Price Action"},
    {"headerName": "Change in Notional Traded", "field": "Change in Notional Traded", "type": "rightAligned", "valueFormatter": {"function": "d3.format('.2%')(params.value)"}},
    {"headerName": "Skew", "field": "Skew", "type": "rightAligned", "valueFormatter": {"function": "d3.format('.2%')(params.value)"}},
    {"headerName": "Comments", "field": "Comments"},
]

defaultColDef = {
    "resizable": True,
    "sortable": True,
    "editable": False,
    "minWidth": 125,
}

grid = dag.AgGrid(
    id="portfolio-grid",
    className="ag-theme-alpine-dark",
    columnDefs=columnDefs,
    rowData=table_data,
    columnSize="sizeToFit",
    defaultColDef=defaultColDef,
    dashGridOptions={"rowSelection": "single", "rowHeight": "45"},
    style={"height": 200},
)

main_chart = dmc.Card(dcc.Graph(id="notional-oi-chart"), withBorder=True)
stats_card = dmc.Card(
    dmc.Stack(
        [
            dmc.Title("Put-Call Ratio & Stats", order=4),
            html.Div(id="put-call-stats", style={"font-size": "1.1rem"}),
        ]
    ),
    withBorder=True,
    p="md",
    style={"minHeight": 300},
)
header = dmc.Title("Options Analytics Dashboard", order=1, ta="center", p="xl", c="blue")

app.layout = dmc.MantineProvider(
    theme={"colorScheme": "dark"},
    withGlobalClasses=True,
    children=html.Div(
        [
            header,
            dmc.Grid([dmc.GridCol(main_chart, span=8), dmc.GridCol(stats_card, span=4)]),
            html.Div(grid),
        ],
        style={"padding": 12},
    ),
)


@app.callback(
    Output("notional-oi-chart", "figure"),
    Output("put-call-stats", "children"),
    Input("portfolio-grid", "selectedRows"),
)
def update_option_analytics(selected_row):
    if not selected_row:
        ticker = "AAPL"
    else:
        ticker = selected_row[0]["Ticker"]

    df = option_data.get(ticker)
    if df is None:
        return go.Figure(), "No data available."

    # Main chart: Notional Traded, Put OI, Call OI
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Notional Traded"], mode="lines+markers", name="Notional Traded"))
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Put OI"], mode="lines", name="Put Open Interest"))
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Call OI"], mode="lines", name="Call Open Interest"))
    fig.update_layout(
        title=f"{ticker} - Notional, Put OI, Call OI (Last 30 days)",
        legend=dict(x=0.01, y=0.99, bgcolor="rgba(0,0,0,0)"),
        template="plotly_dark",
        margin=dict(l=20, r=20, t=40, b=20),
    )

    # Stats card
    latest = df.iloc[-1]
    put_call_ratio = latest["Put OI"] / latest["Call OI"] if latest["Call OI"] else float("nan")
    total_oi = latest["Put OI"] + latest["Call OI"]
    put_pct = 100 * latest["Put OI"] / total_oi if total_oi else float("nan")
    stats = [
        f"Put-Call Ratio: <b>{put_call_ratio:.2f}</b>",
        f"Put OI % of Total OI: <b>{put_pct:.1f}%</b>",
    ]

    return fig, html.Ul([html.Li(html.Span(d, style={"font-size": "1.1em"})) for d in stats])


if __name__ == "__main__":
    app.run(debug=True)
