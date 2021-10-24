from datetime import date
from config import Config
import pandas as pd
import requests
import json
import time


cfg = Config()

with open('strava_tokens.json') as json_file:
        strava_tokens = json.load(json_file)

def refresh_tokens(strava_tokens):

    if strava_tokens['expires_at'] < time.time():

        response = requests.post(
                            url = 'https://www.strava.com/oauth/token',
                            data = {
                                    'client_id': cfg.client_id,
                                    'client_secret': cfg.client_secret,
                                    'grant_type': 'refresh_token',
                                    'refresh_token': strava_tokens['refresh_token']
                                    }
                        )

        new_strava_tokens = response.json()

        with open('strava_tokens.json', 'w') as outfile:
            json.dump(new_strava_tokens, outfile)


def extract_transform():

    page = 1

    url = f"https://www.strava.com/api/v3/clubs/{cfg.club_id}/activities"
    refresh_tokens(strava_tokens)
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
            activities.loc[x + (page-1)*200,'date'] = date.today().strftime('%Y-%m-%d')
        
        page += 1
    activities.to_csv(f"{cfg.output_filename}_{date.today().strftime('%Y-%m-%d')}.csv", index=False)