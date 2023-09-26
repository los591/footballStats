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

## Fetch fixture ids for the current day

def fetchFixturesDate(api_key, api_host, current_date):
    dayFixtures = []
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    #currentDate = '2023-09-02'
    #currentDate = datetime.now().strftime("%Y-%m-%d")
    querystring = {"date":current_date, "league": leagueId, "season":2023}
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
    
    fixtureInfo = r.get(url, headers=headers, params=querystring).json()['response']
    for x in fixtureInfo:
        x['fixture_id'] = fixtureId
    return fixtureInfo

def formatPlayerMetrics(fixtureInfo):
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

## For joining match outcome information

def fetch_fixture_results(api_key, api_host, league, season):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"league":league,"season":season}
    headers = {
        "X-RapidAPI-Key": "d84cd3a986msh99290296f083073p12e132jsnfac9c2bd37bb",
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    response = r.get(url, headers=headers, params=querystring).json()['response']
    fixture_results = []
    for x in response:
        fixture_info = {}
        fixture_info['id'] = x['fixture']['id']
        fixture_info['date'] = x['fixture']['date']
        fixture_info['stadium_name'] = x['fixture']['venue']['name']
        fixture_info['stadium_id'] = x['fixture']['venue']['id']
        fixture_info['home_name'] = x['teams']['home']['name']
        fixture_info['home_id'] = x['teams']['home']['id']
        fixture_info['away_name'] = x['teams']['away']['name']
        fixture_info['away_id'] = x['teams']['away']['id']
        ### This part would need to be adjusted for leagues that have extra time
        fixture_info['home_goals'] = x['score']['fulltime']['home']
        fixture_info['away_goals'] = x['score']['fulltime']['away']
        fixture_results.append(fixture_info)
    return fixture_results

def join_with_match_results(player_info, season_results):
    for x in player_info:
        fixture_id = x['fixture_id']
        for y in season_results:
            if y['id'] == fixture_id:
                x['fixture_info'] = y
                break
    for x in player_info:
        ### Home Away Status
        if x['fixture_info']['home_id'] == x['teamId']:
            x['home'] = 1
        elif x['fixture_info']['away_id'] == x['teamId']:
            x['home'] = 0
        ### Team Success Status
        if x['fixture_info']['home_goals'] > x['fixture_info']['away_goals']:
            if x['home'] == 1:
                x['won'] = 1
            elif x['home'] == 0:
                x['won'] = 0
        elif x['fixture_info']['away_goals'] > x['fixture_info']['home_goals']:
            if x['home'] == 0:
                x['won'] = 1
            elif x['home'] == 1:
                x['won'] = 0
        elif x['fixture_info']['away_goals'] == x['fixture_info']['home_goals']:
            if x['home'] == 0:
                x['won'] = 1
            elif x['home'] == 1:
                x['won'] = 0
        x.pop('fixture_info')
    return player_info




### Global Info

base_url = "https://api-football-v1.p.rapidapi.com/v3"
api_key = "ENTER HERE"
api_host = "ENTER HERE"

leagueId  = fetchLeagueIdByName(api_key, api_host)

season = '2023'

season_results = fetch_fixture_results(api_key, api_host, leagueId, season)

dates = ['2023-09-25','2023-09-24','2023-09-23', '2023-09-22']

allGames = []

for x in dates:
    fixtureIds = fetchFixturesDate(api_key, api_host, x)
    allGames.extend(fixtureIds)

print (allGames)

finalPlayerInfo = []
for x in allGames:
    gameInfo = fetchFixtureById(api_key, api_host, x)
    playerStats = formatPlayerMetrics(gameInfo)
    finalPlayerInfo.extend(playerStats)

fullPlayerInfo = join_with_match_results(finalPlayerInfo, season_results)

### Export to a .xlsx file
df_allPlayers = pd.DataFrame(fullPlayerInfo)
df_allPlayers.to_excel('bundesliga_09_25.xlsx', index=False)
print ("All finished")