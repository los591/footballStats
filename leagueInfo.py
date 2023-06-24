import requests

url = "https://api-football-v1.p.rapidapi.com/v3/leagues"

headers = {
    "X-RapidAPI-Key": "d84cd3a986msh99290296f083073p12e132jsnfac9c2bd37bb",
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

#params = {'team': '33', 'season': '2022'}

response = requests.get(url, headers=headers).json()['response']

leagues = []

for x in response:
    data = {'leagueName': x['league']['name'],
            'leagueId': x['league']['id'],
            'leagueCountry': x['country']['name'],
            'numSeasons': len(x['seasons']),
            'mostRecentSeason': x['seasons'][0]} 
    leagues.append(data)

print ('hello')

print ('hola')