import pandas as pd
import requests
import json
import time


with open('strava_tokens.json') as json_file:
    strava_tokens = json.load(json_file)

if strava_tokens['expires_at'] < time.time():

    response = requests.post(
                        url = 'https://www.strava.com/oauth/token',
                        data = {
                                'client_id': 71997,
                                'client_secret': '141a49ea8777e60efb5790b9b3d88a6f3d9b97ad',
                                'grant_type': 'refresh_token',
                                'refresh_token': strava_tokens['refresh_token']
                                }
                    )

    new_strava_tokens = response.json()

    with open('strava_tokens.json', 'w') as outfile:
        json.dump(new_strava_tokens, outfile)

    strava_tokens = new_strava_tokens

page = 1
id_club = 980426
url = f"https://www.strava.com/api/v3/clubs/{id_club}/activities"
access_token = strava_tokens['access_token']

activities = pd.DataFrame(
    columns = [
            "resource_state",
            "firstname",
            "lastname",
            "name",
            "distance",
            "moving_time",
            "elapsed_time",
            "total_elevation_gain",
            "type"
    ]
)

while True:
    
    r = requests.get(url + '?access_token=' + access_token + '&per_page=200' + '&page=' + str(page))
    r = r.json()

    if (not r):
        break
  
    for x in range(len(r)):
        activities.loc[x + (page-1)*200,'resource_state'] = r[x]['resource_state']
        activities.loc[x + (page-1)*200,'firstname'] = r[x]['athlete']['firstname']
        activities.loc[x + (page-1)*200,'lastname'] = r[x]['athlete']['lastname']
        activities.loc[x + (page-1)*200,'name'] = r[x]['name']
        activities.loc[x + (page-1)*200,'distance'] = r[x]['distance']
        activities.loc[x + (page-1)*200,'moving_time'] = r[x]['moving_time']
        activities.loc[x + (page-1)*200,'elapsed_time'] = r[x]['elapsed_time']
        activities.loc[x + (page-1)*200,'total_elevation_gain'] = r[x]['total_elevation_gain']
        activities.loc[x + (page-1)*200,'type'] = r[x]['type']
      
    page += 1
activities.to_csv('codeRunner_activities.csv', index=False)





