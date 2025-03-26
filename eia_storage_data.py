import requests
import pandas as pd


def main():
  # Replace with your EIA API key
  API_KEY = "YhzkKpmhTYHId1ed4EQUrqYXBYOATxUd46yc2D5n"

  params = {
      "api_key": API_KEY,
      "frequency": "weekly",
      'data[]':'value',
      "start": "2019-01-01",
      "end": "2025-04-01",
      "facets[series][]": "NW2_EPG0_SWO_R48_BCF"
      # "facets[series][]": "Total U.S."  # or use specific regions if desired
  }

  url = f"https://api.eia.gov/v2/natural-gas/stor/wkly/data/"

  response = requests.get(url, params=params)
  data = response.json()

  results = data['response']['data']
  df = pd.DataFrame(results)

  series = df[['period','value']]
  series['value'] = pd.to_numeric(series['value'], errors='coerce')
  series['diff'] = series['value'].diff()
  series.to_csv('data/eia_storage.csv')

if __name__ == '__main__':
  main()