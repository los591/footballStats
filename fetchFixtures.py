import requests as r
import pandas as pd
from datetime import datetime, date, timedelta

### Get Premier League Id

def fetchLeagueIdByName(api_key, api_host):
    leagueCountry = input("Type the country of the League you want to follow")
    leagueName = input("Type the name of the League you want to follow")
    #Make the call
    url = "https://api-football-v1.p.rapidapi.com/v3/leagues"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": api_host
    }
    params = {"country":leagueCountry}
    response = r.get(url, headers=headers, params = params).json()['response']
    print ("all leagues fetched")
    for x in response:
        if x['league']['name'] == leagueName:
            leagueId = x['league']['id']
            break
        else:
            #print ('league not found')
            pass
    return leagueId


def fetch_fixtures_by_date(api_key, api_host, league_id, season):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"league":league_id,"season":season}
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": api_host
    }
    response = r.get(url, headers=headers, params=querystring).json()['response']
    return response

def format_dedupe_dates(raw_chart):
    all_dates = [x['fixture']['date'][0:10] for x in raw_chart]
    deduped = []
    for x in all_dates:
        if x not in deduped:
            deduped.append(x)
        else:
            pass
    return deduped


### Global Info

base_url = "ENTER"
api_key = "ENTER"
api_host = "api-football-v1.p.rapidapi.com"

league_id  = fetchLeagueIdByName(api_key, api_host)
season = 2022


test2 = fetch_fixtures_by_date(api_key, api_host, league_id, season)

dedupes = format_dedupe_dates(test2)


print ("hello")