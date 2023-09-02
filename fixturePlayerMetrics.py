import requests as r
import pandas as pd
from datetime import datetime, date

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

## Fetch fixture ids for the current day

def fetchFixturesDate(api_key, api_host):
    dayFixtures = []
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    currentDate = datetime.now().strftime("%Y-%m-%d")
    querystring = {"date":currentDate, "league": leagueId, "season":2023}
    headers = {
    	"X-RapidAPI-Key": api_key,
    	"X-RapidAPI-Host": api_host
    }
    response = r.get(url, headers=headers, params=querystring).json()['response']
    for x in response:
        fixtureId = x['fixture']['id']
        dayFixtures.append(fixtureId)
    return dayFixtures

## Fetch fixture statistics using a fixture id

def fetchFixtureById(api_key, api_host, fixtureId):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/players"
    
    querystring = {"fixture":fixtureId}
    
    headers = {
    	"X-RapidAPI-Key": api_key,
    	"X-RapidAPI-Host": api_host
    }
    
    response = r.get(url, headers=headers, params=querystring).json()['response']
    
    playerInfo = []
    
    for x in response:
        playerData = []
        for y in x['players']:
            y['teamName'] =  x['team']['name']
            y['teamId'] = x['team']['id']
            playerData.append(y)
        playerInfo.extend(playerData)
        
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
            'goalsAssisted': x['statistics'][0]['goals']['assists']                 
        }
        playerStats.append(playerRaw)
    return playerStats
        
        

### Global Info

base_url = "https://api-football-v1.p.rapidapi.com/v3"
api_key = "ENTER YOUR API KEY"
api_host = "ENTER YOUR HOST"

leagueId  = fetchLeagueIdByName(api_key, api_host)

fixtureIds = fetchFixturesDate(api_key, api_host)

finalPlayerInfo = []
for x in fixtureIds:
    gameInfo = fetchFixtureById(api_key, api_host, x)
    finalPlayerInfo.extend(gameInfo)

### Export to a .xlsx file
df_allPlayers = pd.DataFrame(finalPlayerInfo)
df_allPlayers.to_excel('playerMatchMetrics1.xlsx', index=False)
print ("All finished")
