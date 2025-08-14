import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

def pull_data_from_driver_averages(url, driver_in_first):
    # send the HTTP request
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    # parse the HTML of the webpage
    soup = BeautifulSoup(response.content, 'html.parser')

    # find all <table> html objects
    tables = soup.find_all("table")

    # check how many tables there are (how many we'll have to iterate through in the next cell)
    print(f"Found {len(tables)} tables.")

    # loop through found tables and save the correct one as a pandas df
    for i in range(len(tables)):
        try:
            html_str = str(tables[i])
            temp = pd.read_html(StringIO(html_str))[0]
            if "Driver" in temp.columns:
                if temp.iloc[0]["Driver"] == driver_in_first: ## change this line to the best driver as of recent in the table
                    track_stats = temp
                    break
        except Exception as e:
            print(f"Skipping table {i}: {e}")

    track_stats.columns = track_stats.columns.str.replace("  ", " ", regex=False).str.strip()
    for col in track_stats.columns:
        if "Unnamed" in col:
            track_stats = track_stats.drop(columns=[col])
    
    return track_stats

def pull_season_stats(url="https://www.driveraverages.com/nascar/nascar-stats.php", driver_in_first=""):
    # send the HTTP request
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    # parse the HTML of the webpage
    soup = BeautifulSoup(response.content, 'html.parser')

    # find all <table> html objects
    tables = soup.find_all("table")

    for i in range(len(tables)):
        try:
            html_str = str(tables[i])
            temp = pd.read_html(StringIO(html_str))[0]
            if "Driver" in temp.columns:
                if temp.iloc[0]["Driver"] == driver_in_first: ## change this line to the best driver as of recent in the season points
                    season_stats = temp
                    break
        except Exception as e:
            print(f"Skipping table {i}: {e}")

    season_stats.columns = season_stats.columns.str.replace("  ", " ", regex=False).str.strip()
    season_stats = season_stats.drop(columns=["NASCAR Points", "Top 10's"])
    for col in season_stats.columns:
        if "Unnamed" in col:
            season_stats = season_stats.drop(columns=[col])

    season_stats = season_stats.rename(
        columns={col: f"szn_{col}" for col in season_stats.columns if col != "Driver"}
    )

    return season_stats