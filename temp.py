import pandas as pd

# Sample data based on your input
data = """
MARKET          : SOM   - STOCK OPTIONS                   
UNDERLYING      : CSE   
EXPIRATION DATE : 30 JUL 25

         < ------------------  CALL OPTIONS  ------------------------ > < -------------------  PUT OPTIONS  ----------------------- >
                             NET                      SETTLE   PRICE                        NET                       SETTLE   PRICE
 STRIKE    GROSS    NET     CHANGE    T/O     DEAL    PRICE    CHANGE    GROSS     NET     CHANGE     T/O    DEAL     PRICE    CHANGE
-------- -------- -------- --------- ------- ------- --------- -------- -------- -------- --------- ------- ------- --------- --------
   20.00        0        0         0       0       0     11.19     0.31        0        0         0       0       0      0.01     0.00
   21.00        0        0         0       0       0     10.07     0.25        0        0         0       0       0      0.01     0.00
   22.00        0        0         0       0       0      9.19     0.37        2        2         0       0       0      0.01     0.00
   23.00        0        0         0       0       0      8.02     0.20       92       92         0       0       0      0.01     0.00
   24.00        0        0         0       0       0      7.07     0.25      430      400         0       0       0      0.01     0.00
   25.00        0        0         0       0       0      6.02     0.18       90       90         0       0       0      0.01     0.00
   26.00       80       70         0       0       0      5.17     0.35      378      291         0       0       0      0.01     0.00
   27.00      250      250         0       0       0      4.15     0.21      382      246         0       0       0      0.01     0.00
   28.00       55       50         0       0       0      3.14     0.28      804      730         0       0       0      0.03     0.00
   29.00      100       40         0       0       0      2.19     0.28      819      627       -10      20       2      0.10    -0.01
   30.00      969      967        40      41       6      1.31     0.17    2302     2107      -101     123       7      0.29    -0.04
   31.00     1615     1463        12     110       6      0.73     0.15    1911     1594        31      72       6      0.68    -0.10
   32.00      878      681         0      28       4      0.34     0.08      592      434       -27      38       2      1.30    -0.17
   33.00     1025      912       -25      65       3      0.13     0.04     1183     1156         0       0       0      2.12    -0.22
   34.00      590      478         0       0       0      0.05     0.02      509      441         0      80       3      3.03    -0.19
   35.00      567      539         0       0       0      0.02     0.01       71       60         0       0       0      4.00    -0.33
   36.00      328      321         0       0       0      0.01     0.00      210      180         0       0       0      5.00    -0.20
   37.00      413      381         0       0       0      0.01     0.00        0        0         0       0       0      6.00    -0.39
   38.00      392      392         0       0       0      0.01     0.00        0        0         0       0       0      7.00    -0.21
   39.00      314      199         0       0       0      0.01     0.00        0        0         0       0       0      8.00    -0.20
   40.00       32       32         0       0       0      0.01     0.00        0        0         0       0       0      9.00    -0.27
"""

# Extract underlying and expiration date
lines = data.strip().split('\n')
underlying = lines[1].split(':')[1].strip()
exp_date = lines[2].split(':')[1].strip()

# Parse the data into lists
rows = []
for line in lines[7:]:  # Skip header lines
    if line.strip() and not line.startswith('----') and not line.startswith('TOTAL'):
        parts = line.split()
        strike = float(parts[0])
        call_gross = int(parts[1].replace(',', ''))
        call_settle = float(parts[6])
        put_gross = int(parts[8].replace(',', ''))
        put_settle = float(parts[13])
        
        # Add call option if gross is non-zero
        if call_gross > 0:
            option_name = f"{underlying} Call {strike:.0f} {exp_date}"
            rows.append([option_name, call_gross, call_settle])
        
        # Add put option if gross is non-zero
        if put_gross > 0:
            option_name = f"{underlying} Put {strike:.0f} {exp_date}"
            rows.append([option_name, put_gross, put_settle])

# Create DataFrame
df = pd.DataFrame(rows, columns=["Option", "Gross", "Settle Price"])

# Display the DataFrame
print(df)

#-------

import pandas as pd
import re

def process_option_chain(lines, start_idx):
    # Extract header information
    underlying = lines[start_idx + 1].split(':')[1].strip()
    exp_date = lines[start_idx + 2].split(':')[1].strip()

    # Find the start of data (skip headers until STRIKE line)
    data_start = start_idx + 7
    while data_start < len(lines) and not lines[data_start].startswith(' STRIKE'):
        data_start += 1
    if data_start >= len(lines):
        return None, start_idx

    # Initialize lists for DataFrame
    rows = []
    
    # Process data lines until 'TOTAL' or end of file
    for i in range(data_start + 2, len(lines)):
        line = lines[i].strip()
        if not line or line.startswith('----') or line.startswith('TOTAL'):
            return pd.DataFrame(rows, columns=["Option", "Gross", "Settle Price"]), i
        if line.startswith('MARKET'):
            return pd.DataFrame(rows, columns=["Option", "Gross", "Settle Price"]), i - 1

        # Parse the line
        parts = line.split()
        if len(parts) < 14:
            continue  # Skip malformed lines
        try:
            strike = float(parts[0])
            call_gross = int(parts[1].replace(',', ''))
            call_settle = float(parts[6])
            put_gross = int(parts[8].replace(',', ''))
            put_settle = float(parts[13])

            # Add call option if gross is non-zero
            if call_gross > 0:
                option_name = f"{underlying} Call {strike:.0f} {exp_date}"
                rows.append([option_name, call_gross, call_settle])

            # Add put option if gross is non-zero
            if put_gross > 0:
                option_name = f"{underlying} Put {strike:.0f} {exp_date}"
                rows.append([option_name, put_gross, put_settle])
        except (ValueError, IndexError):
            continue  # Skip lines that can't be parsed

    return pd.DataFrame(rows, columns=["Option", "Gross", "Settle Price"]), len(lines)

# Read the file and process all option chains
def process_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    all_dfs = []
    i = 0
    while i < len(lines):
        if lines[i].startswith('MARKET          : SOM   - STOCK OPTIONS'):
            df, new_idx = process_option_chain(lines, i)
            if df is not None and not df.empty:
                all_dfs.append(df)
            i = new_idx + 1
        else:
            i += 1

    # Combine all DataFrames
    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    return pd.DataFrame(columns=["Option", "Gross", "Settle Price"])

# Example usage
file_path = 'your_file.txt'  # Replace with your file path
result_df = process_file(file_path)
print(result_df)
