import requests as r
import pandas as pd
import getpass as getpass

BASE_URL = "https://api-football-v1.p.rapidapi.com/v3"


### Leagues Endpoints: Use in order to fetch the league info you are interested in. In practice, you will use this just for the league id, which you need in order to retrieve statistics using other endpoints
# Note that there are some restrictions for the parameters used, such as using "search" and "name" at the same time. Recommendation is to enter the country and name of the league

def fetch_leagues(api_key:str, api_host:str, country: str):#, league_name: str):
    url = BASE_URL + "/leagues"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": api_host
    }
    params = {"country":country,
              #"name": league_name
              }
    return r.get(url, headers=headers, params = params).json()

'''
    "search":"ligapro"
    "name":"Premier League"
    "current":"true"
    "season":"2022"
    "code":"uk"
    "country":"England"
    "team":"33"
    "last":"1"
    "type":"league"

'''



def fetch_leagues_by_country(api_key, api_host):
    league_country = input("Type the country of the League you want to follow")
    #Make the call
    url = BASE_URL + "/leagues"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": api_host
    }
    params = {"country":league_country}
    return r.get(url, headers=headers, params = params).json()


def fetch_league_id_by_name(api_key, api_host):
    league_country = input("Type the country of the League you want to follow")
    league_name = input("Type the name of the League you want to follow")
    #Make the call
    url = "https://api-football-v1.p.rapidapi.com/v3/leagues"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": api_host
    }
    params = {"country":league_country}
    response = r.get(url, headers=headers, params = params).json()['response']
    print ("all leagues fetched")
    for x in response:
        if x['league']['name'] == league_name:
            league_id = x['league']['id']
            break
        else:
            print ('league not found')
            pass
    return league_id

## Fetch fixture ids for the current day. Returns a list with the fixture ids 
def fetch_fixture_ids_by_date(api_key:str, api_host:str, date:str, league_id:str, season: str):
    dayFixtures = []
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    #currentDate = '2023-09-02'
    #currentDate = datetime.now().strftime("%Y-%m-%d")
    querystring = {"date":date, "league": league_id, "season":season}
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": api_host
    }
    response = r.get(url, headers=headers, params=querystring).json()['response']
    for x in response:
        fixtureId = x['fixture']['id']
        dayFixtures.append(fixtureId)
    return dayFixtures

# Fetch a match information based on the fixture id. This contains all the player, match-level performance metrics

def fetch_fixture_info_by_id(api_key:str, api_host:str, fixtureId: int):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/players"
    
    querystring = {"fixture":fixtureId}
    
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": api_host
    }
    
    fixtureCall = r.get(url, headers=headers, params=querystring)
    fixtureInfo = fixtureCall.json()['response']
    for x in fixtureInfo:
        x['fixture_id'] = fixtureId
    return fixtureInfo

# Fetch match results for an entire season

def fetch_season_fixture_results(api_key, api_host, league_id, season):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"league":league_id,"season":season}
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": api_host
    }       
    return r.get(url, headers=headers, params=querystring).json()['response']

# Fetches all the dates where games took place. Useful if you need to do a large download of player information
def fetch_fixture_dates_by_season(api_key, api_host, league_id, season):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"league":league_id,"season":season}
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": api_host
    }
    response = r.get(url, headers=headers, params=querystring).json()['response']
    return response

def formatPlayerMetrics(self, fixtureInfo, season):
### THIS NEEDS TO BE SPLIT IN TWO FUNCTIONS
### Make sure each player dictionary retains the team information and the fixture id
    playerInfo = []
    for x in fixtureInfo:
        playerData = []
        fixture_id = x['fixture_id']
        for y in x['players']:
            y['teamName'] =  x['team']['name']
            y['teamId'] = x['team']['id']
            y['fixture_id'] = fixture_id
            y['season'] = season
            playerData.append(y)
        playerInfo.extend(playerData)
    ### Now we construct each player's dictionary. 
    playerStats = []
    for x in playerInfo:
        if x['statistics'][0]['games']['substitute'] == False:
            starter = True
        elif x['statistics'][0]['games']['substitute'] == True:
            starter = False
        playerRaw = {
            ### General Information
            'playerName': x['player']['name'],
            'playerId': x['player']['id'],
            'fixture_id': x['fixture_id'],
            'position': x['statistics'][0]['games']['position'],
            'teamName': x['teamName'],
            'teamId': x['teamId'],
            'jerseyNumber': x['statistics'][0]['games']['number'],
            ### Match Info
            'minutesPlayed': x['statistics'][0]['games']['minutes'],
            'captain': x['statistics'][0]['games']['captain'],
            'starter': starter,
            'offsides': x['statistics'][0]['offsides'],
            ### Scoring related metrics
            'goalsScored':x['statistics'][0]['goals']['total'],
            'goalsAssisted': x['statistics'][0]['goals']['assists'],
            'goalsConceded': x['statistics'][0]['goals']['conceded'],
            'goalsSaved': x['statistics'][0]['goals']['saves'],
            ### Shots
            'totalShots': x['statistics'][0]['shots']['total'],
            'shotsOnTarget': x['statistics'][0]['shots']['on'],
            ### Passing related metrics
            'totalPasses': x['statistics'][0]['passes']['total'],
            'AccuratePasses': int(x['statistics'][0]['passes']['accuracy']) if x['statistics'][0]['passes']['accuracy'] != None else -1,
            'KeyPasses': x['statistics'][0]['passes']['key'],
            'passAccuracy':  int(x['statistics'][0]['passes']['accuracy']) / x['statistics'][0]['passes']['total'] if x['statistics'][0]['passes']['total'] != 0 and x['statistics'][0]['passes']['accuracy'] != None else -1,
            ### Tackles
            'totalTackles': x['statistics'][0]['tackles']['total'],
            'totalBlocks': x['statistics'][0]['tackles']['blocks'],
            'totalInterceptions': x['statistics'][0]['tackles']['interceptions'],
            ### Duels
            'totalDuels': x['statistics'][0]['duels']['total'],
            'duelsWon': x['statistics'][0]['duels']['won'],
            ### Dribbles
            'attemptedDribbles': x['statistics'][0]['dribbles']['attempts'],
            'successfulDribbles': x['statistics'][0]['dribbles']['success'],
            ### Fouls
            'foulsDrawn': x['statistics'][0]['fouls']['drawn'],
            'foulsCommitted': x['statistics'][0]['fouls']['committed'],
            ### Cards
            'totalYellowCards': x['statistics'][0]['cards']['yellow'],
            'totalRedCards': x['statistics'][0]['cards']['red'],
            ### Penalties
            'penaltiesDrawn': x['statistics'][0]['penalty']['won'],
            'penaltiesCommitted': x['statistics'][0]['penalty']['commited'],
            'penaltiesScored': x['statistics'][0]['penalty']['scored'],
            'penaltiesMissed': x['statistics'][0]['penalty']['missed'],
            'penaltiesSaved': x['statistics'][0]['penalty']['saved']

                            
        }
        playerStats.append(playerRaw)
    return playerStats
