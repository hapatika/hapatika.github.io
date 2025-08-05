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
'''
Note the full path, e.g., C:\Users\YourUser\Anaconda3\python.exe or C:\Python39\python.exe.
3. Open Windows Task Scheduler
Press Win + S and type Task Scheduler, then open it.
4. Create a Basic Task
Action > Create Basic Task…
Give your task a name (e.g., “Download HKEX Data”).
Trigger: Choose Daily (or whatever schedule you want).
Start time: Set the time (e.g., 12:10 PM for after morning close).
If you want it twice a day, you’ll need to create two tasks, or use “Repeat task every...”.
Action: Select Start a program.
5. Set the Program and Arguments
Program/script:
Enter the path to your python executable, for example:
C:\Users\YourUser\Anaconda3\python.exe
C:\path\to\your_script.py
7. For Running the Script Multiple Times Per Day
In “Create Basic Task”, after finishing, double-click your task in the Task Scheduler Library.
Go to the Triggers tab, click Edit, and set:
"Repeat task every:" (e.g., 4 hours) and "for a duration of:" (e.g., 1 day).
Or, create multiple triggers (e.g., one for 12:10, one for 16:10).
'''
