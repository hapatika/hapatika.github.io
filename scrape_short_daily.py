import requests
import datetime
import os

# HKEX short selling data URL
url = "https://www.hkex.com.hk/eng/stat/smstat/ssturnover/ncms/mshtmain.htm"

# Create a folder to save data
save_folder = "hkex_short_selling"
os.makedirs(save_folder, exist_ok=True)

# Current date and time for filename
now = datetime.datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M")

# File path
file_path = os.path.join(save_folder, f"short_selling_{timestamp}.html")

# Download and save the data
try:
    response = requests.get(url)
    response.raise_for_status()
    with open(file_path, 'w', encoding="utf-8") as f:
        f.write(response.text)
    print(f"Downloaded and saved: {file_path}")
except Exception as e:
    print(f"Failed to download: {e}")

# BS4

from bs4 import BeautifulSoup

# ... [previous code up to response.text]

soup = BeautifulSoup(response.text, 'html.parser')
# Find the main table (adjust selector as needed)
table = soup.find("table")
if table:
    table_html = str(table)
    with open(file_path.replace('.html', '_table.html'), 'w', encoding='utf-8') as f:
        f.write(table_html)
    print(f"Table saved: {file_path.replace('.html', '_table.html')}")
else:
    print("Table not found in HTML.")

# Schedule on windows 
