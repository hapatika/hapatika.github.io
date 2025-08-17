import dash
from dash import dcc, html, Input, Output, State
import dash_table
import plotly.graph_objs as go
import pandas as pd
import numpy as np

# Example data (replace with your real data)
np.random.seed(42)
dates = pd.date_range('2024-08-01', periods=20)
stocks = ['BYD (1211 HK)', 'Tencent (700 HK)', 'Meituan (3690 HK)']
data = []
for date in dates:
    for stock in stocks:
        sst = np.random.normal(0, 1)
        put_change = np.random.normal(0, 1)
        call_change = np.random.normal(0, 1)
        price = np.random.normal(0, 1)
        # Event flagging logic
        if sst > 0.8 and put_change > 0.5 and price < -0.5:
            event_type = 'Type 1'
        elif sst > 0.8 and put_change > 0.5 and price > 0.5:
            event_type = 'Type 2'
        elif sst > 0.8 and call_change < -0.5 and price > 0.5:
            event_type = 'Type 3'
        else:
            event_type = None
        if event_type:
            data.append({
                'Date': date.strftime('%Y-%m-%d'),
                'Stock': stock,
                'Short Selling Turnover Δ (%)': round(sst*30 + 30, 1),
                'Put OI Δ (%)': round(put_change*20 + 10, 1),
                'Call OI Δ (%)': round(call_change*15, 1),
                'Price Δ (%)': round(price*2, 2),
                'Event Type': event_type
            })
df = pd.DataFrame(data)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("Short Selling × Options Interest Event Screener"),
    dash_table.DataTable(
        id='events-table',
        columns=[
            {'name': 'Date', 'id': 'Date'},
            {'name': 'Stock', 'id': 'Stock'},
            {'name': 'Short Selling Turnover Δ (%)', 'id': 'Short Selling Turnover Δ (%)'},
            {'name': 'Put OI Δ (%)', 'id': 'Put OI Δ (%)'},
            {'name': 'Call OI Δ (%)', 'id': 'Call OI Δ (%)'},
            {'name': 'Price Δ (%)', 'id': 'Price Δ (%)'},
            {'name': 'Event Type', 'id': 'Event Type'},
        ],
        data=df.to_dict('records'),
        style_cell={'textAlign': 'center', 'fontSize':14},
        style_data_conditional=[
            {'if': {'column_id': 'Price Δ (%)', 'filter_query': '{Price Δ (%)} < 0'},
             'color': 'red'},
            {'if': {'column_id': 'Price Δ (%)', 'filter_query': '{Price Δ (%)} > 0'},
             'color': 'green'},
            {'if': {'column_id': 'Event Type', 'filter_query': '{Event Type} = "Type 1"'},
             'backgroundColor': '#ffe4e1'},
            {'if': {'column_id': 'Event Type', 'filter_query': '{Event Type} = "Type 2"'},
             'backgroundColor': '#e0f7fa'},
            {'if': {'column_id': 'Event Type', 'filter_query': '{Event Type} = "Type 3"'},
             'backgroundColor': '#e8f5e9'},
        ],
        row_selectable='single',
        selected_rows=[],
        page_size=8,
    ),
    html.Div(id='details-panel', style={'marginTop':'30px'})
])

@app.callback(
    Output('details-panel', 'children'),
    Input('events-table', 'selected_rows'),
    State('events-table', 'data')
)
def show_details(selected_rows, table_data):
    if not selected_rows:
        return ""
    row = table_data[selected_rows[0]]
    # Fake time series for charts
    days = pd.date_range(pd.to_datetime(row['Date']) - pd.Timedelta(days=2), periods=3)
    sst_series = np.random.normal(loc=row['Short Selling Turnover Δ (%)']-10, scale=3, size=3)
    put_series = np.random.normal(loc=row['Put OI Δ (%)']-2, scale=2, size=3)
    call_series = np.random.normal(loc=row['Call OI Δ (%)']+2, scale=2, size=3)
    price_series = np.cumsum(np.random.normal(loc=row['Price Δ (%)']/3, scale=0.5, size=3)) + 100

    fig = go.Figure()
    fig.add_trace(go.Bar(x=days, y=sst_series, name='Short Selling Turnover Δ (%)', marker_color='#888'))
    fig.add_trace(go.Scatter(x=days, y=put_series, name='Put OI Δ (%)', mode='lines+markers', marker_color='#1976d2'))
    fig.add_trace(go.Scatter(x=days, y=call_series, name='Call OI Δ (%)', mode='lines+markers', marker_color='#ff9800'))
    fig.add_trace(go.Scatter(x=days, y=price_series, name='Price', mode='lines+markers', marker_color='green', yaxis='y2'))

    fig.update_layout(
        title="3-Day Event Context",
        xaxis_title="Date",
        yaxis=dict(title="Δ (%)"),
        yaxis2=dict(title="Price", overlaying='y', side='right', showgrid=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=400, template='plotly_white'
    )
    return html.Div([
        html.H4(f"{row['Stock']} on {row['Date']} ({row['Event Type']})"),
        dcc.Graph(figure=fig),
        html.P("Shows three-day trend for short selling turnover, put/call OI change, and spot price. Use this to understand the setup flagged by the event.")
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
