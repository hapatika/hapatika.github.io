import requests
import pandas as pd

# EODHD API setup (replace 'YOUR_API_KEY' with your actual key)
api_key = 'YOUR_API_KEY'
url = f"https://eodhistoricaldata.com/api/upcoming-ipos?api_token={api_key}"

# Fetch upcoming IPOs
response = requests.get(url)
upcoming_ipos = response.json()
df_ipos = pd.DataFrame(upcoming_ipos)

# Filter for Korea and Taiwan (based on exchange or country)
df_korea_taiwan = df_ipos[df_ipos['exchange'].isin(['KRX', 'TWSE', 'TPEX'])]
print(df_korea_taiwan[['name', 'ipo_date', 'price_range', 'shares_offered', 'exchange']])

import requests
from bs4 import BeautifulSoup
import pandas as pd

# KRX IPO calendar page (adjust URL based on actual page)
url = "https://global.krx.co.kr/contents/GLB/02/0201/02010400/GLB02010400.jsp"
headers = {'User-Agent': 'Mozilla/5.0'}  # Avoid bot detection
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Find IPO table (inspect the page to get correct tags/classes)
table = soup.find('table', class_='ipo-table')  # Example class name
rows = table.find_all('tr')[1:]  # Skip header row

ipo_data = []
for row in rows:
    cols = row.find_all('td')
    ipo_data.append({
        'company': cols[0].text.strip(),
        'ipo_date': cols[1].text.strip(),
        'price_range': cols[2].text.strip(),
        'shares': cols[3].text.strip(),
        'exchange': 'KRX'
    })

df_ipos = pd.DataFrame(ipo_data)
print(df_ipos)

'''
4. Process and Store DataOnce you have the data:Clean Data: Handle missing values, standardize date formats (e.g., pd.to_datetime), and convert numerical fields (e.g., shares, price) to appropriate types.
Store Data: Use a lightweight database like SQLite or save to CSV/JSON for simplicity.
Update Mechanism: Schedule periodic updates (e.g., daily) using a cron job or Python’s schedule library.

Example: Data Cleaning and Storage:

'''

import sqlite3
import pandas as pd

# Clean data
df_ipos['ipo_date'] = pd.to_datetime(df_ipos['ipo_date'], errors='coerce')
df_ipos['shares'] = pd.to_numeric(df_ipos['shares'], errors='coerce')
df_ipos.fillna({'price_range': 'N/A', 'shares': 0}, inplace=True)

# Store in SQLite
conn = sqlite3.connect('ipo_database.db')
df_ipos.to_sql('ipos', conn, if_exists='replace', index=False)
conn.close()

import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Sample data (replace with your DataFrame)
df_ipos = pd.read_sql('SELECT * FROM ipos', sqlite3.connect('ipo_database.db'))

app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("APAC IPO Tracker (Korea & Taiwan)"),
    dcc.Dropdown(
        id='exchange-filter',
        options=[{'label': ex, 'value': ex} for ex in df_ipos['exchange'].unique()],
        value=['KRX', 'TWSE', 'TPEX'],
        multi=True
    ),
    dcc.Graph(id='ipo-timeline'),
    html.Table([
        html.Tr([html.Th(col) for col in df_ipos.columns]),
        *[html.Tr([html.Td(df_ipos.iloc[i][col]) for col in df_ipos.columns])
          for i in range(min(len(df_ipos), 10))]
    ])
])

# Callback for interactive timeline
@app.callback(
    dash.dependencies.Output('ipo-timeline', 'figure'),
    [dash.dependencies.Input('exchange-filter', 'value')]
)
def update_graph(selected_exchanges):
    filtered_df = df_ipos[df_ipos['exchange'].isin(selected_exchanges)]
    fig = px.timeline(
        filtered_df,
        x_start='ipo_date',
        x_end='ipo_date',
        y='company',
        color='exchange',
        title='Upcoming IPOs Timeline'
    )
    fig.update_yaxes(autorange='reversed')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)


import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df_ipos = pd.read_sql('SELECT * FROM ipos', sqlite3.connect('ipo_database.db'))

st.title("APAC IPO Tracker (Korea & Taiwan)")
exchanges = st.multiselect("Select Exchanges", df_ipos['exchange'].unique(), default=['KRX', 'TWSE', 'TPEX'])
filtered_df = df_ipos[df_ipos['exchange'].isin(exchanges)]

# Timeline
fig = px.timeline(
    filtered_df,
    x_start='ipo_date',
    x_end='ipo_date',
    y='company',
    color='exchange',
    title='Upcoming IPOs Timeline'
)
fig.update_yaxes(autorange='reversed')
st.plotly_chart(fig)

# Data table
st.dataframe(filtered_df)

# Scheduler 

import schedule
import time

def update_data():
    # Run your API/scraping code here
    print("Updating IPO data...")
    # Example: Fetch and store new data
    # df_ipos = fetch_ipo_data()  # Your function
    # df_ipos.to_sql('ipos', sqlite3.connect('ipo_database.db'), if_exists='replace')

schedule.every().day.at("08:00").do(update_data)

while True:
    schedule.run_pending()
    time.sleep(60)
