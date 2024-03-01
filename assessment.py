import json
import requests
import pandas as pd
import matplotlib.pyplot as plt

url = "https://api.data.gov.my/data-catalogue?id=exchangerates" 

response_json = requests.get(url=url).json()
filtered_json = [item for item in response_json if pd.to_datetime(item['date']) >= pd.to_datetime('2022-01-01')]
data = filtered_json

# Convert to DataFrame
df = pd.DataFrame(data)

# Calculate percent change for each year
df['pct_change_2022_2023'] = (df['myr_usd'].pct_change() * 100).fillna(0)
df['pct_change_2023_2024'] = (df['myr_usd'].pct_change(periods=365) * 100).fillna(0)
df['pct_change_2022_2024'] = (df['myr_usd'].pct_change(periods=365*2) * 100).fillna(0)

# Create separate charts
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 10))

# Chart 1: Percent Change from 2022 to 2023
df.plot(x='date', y='pct_change_2022_2023', ax=axes[0, 0], title='Percent Change from 2022 to 2023')

# Chart 2: Percent Change from 2023 to 2024
df.plot(x='date', y='pct_change_2023_2024', ax=axes[0, 1], title='Percent Change from 2023 to 2024')

# Chart 3: Overall Percent Change from 2022 to 2024
df.plot(x='date', y='pct_change_2022_2024', ax=axes[1, 0], title='Overall Percent Change from 2022 to 2024')

# Chart 4: Trend Over Time
df.plot(x='date', y=['myr_usd'], ax=axes[1, 1], title='MYR to USD Exchange Rate Trend Over Time')

# Display the charts
plt.tight_layout()
plt.show()