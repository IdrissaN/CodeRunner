import pandas as pd
import requests
import json
import time
## Get the tokens from file to connect to Strava
with open('strava_tokens.json') as json_file:
    strava_tokens = json.load(json_file)
if strava_tokens['expires_at'] < time.time():
#Make Strava auth API call with current refresh token
    response = requests.post(
                        url = 'https://www.strava.com/oauth/token',
                        data = {
                                'client_id': 71997,
                                'client_secret': '141a49ea8777e60efb5790b9b3d88a6f3d9b97ad',
                                'grant_type': 'refresh_token',
                                'refresh_token': strava_tokens['refresh_token']
                                }
                    )
#Save response as json in new variable
    new_strava_tokens = response.json()
# Save new tokens to file
    with open('strava_tokens.json', 'w') as outfile:
        json.dump(new_strava_tokens, outfile)

    strava_tokens = new_strava_tokens
#Loop through all activities
page = 1
user_id = 92455812
url = f"https://www.strava.com/api/v3/activities"
access_token = strava_tokens['access_token']

activities = pd.DataFrame(
    columns = [
            "id",
            "name",
            "start_date_local",
            "type",
            "distance",
            "moving_time",
            "elapsed_time",
            "average_speed",
            "max_speed",
            "total_elevation_gain",
            "kudos_count",
            "comment_count",
            "start_latlng",
            "end_latlng",
            "external_id"
    ]
)
while True:
    
    # get page of activities from Strava
    r = requests.get(url + '?access_token=' + access_token + '&per_page=200' + '&page=' + str(page))
    r = r.json()
# if no results then exit loop
    if (not r):
        break
    
    # otherwise add new data to dataframe
    for x in range(len(r)):
        activities.loc[x + (page-1)*200,'id'] = r[x]['id']
        activities.loc[x + (page-1)*200,'name'] = r[x]['name']
        activities.loc[x + (page-1)*200,'start_date_local'] = r[x]['start_date_local']
        activities.loc[x + (page-1)*200,'type'] = r[x]['type']
        activities.loc[x + (page-1)*200,'distance'] = r[x]['distance']
        activities.loc[x + (page-1)*200,'moving_time'] = r[x]['moving_time']
        activities.loc[x + (page-1)*200,'elapsed_time'] = r[x]['elapsed_time']
        activities.loc[x + (page-1)*200,'average_speed'] = r[x]['average_speed']
        activities.loc[x + (page-1)*200,'max_speed'] = r[x]['max_speed']
        activities.loc[x + (page-1)*200,'total_elevation_gain'] = r[x]['total_elevation_gain']
        activities.loc[x + (page-1)*200,'kudos_count'] = r[x]['kudos_count']
        activities.loc[x + (page-1)*200,'comment_count'] = r[x]['comment_count']
        activities.loc[x + (page-1)*200,'start_latlng'] = r[x]['start_latlng']
        activities.loc[x + (page-1)*200,'end_latlng'] = r[x]['end_latlng']
        activities.loc[x + (page-1)*200,'external_id'] = r[x]['external_id']
# increment page
    page += 1
#activities.to_csv(f'user_{user_id}_strava_activities.csv', index=False)
activities.to_csv(f'user_strava_activities.csv', index=False)