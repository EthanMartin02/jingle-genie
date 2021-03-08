import os
import sys
import spotipy
import json
import spotipy.util as util
import random
import tweepy

# Set user ID retreived from Spotify account.
username = os.environ.get('SPOTIPY_USERID')

try:
    token = util.prompt_for_user_token(username)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)

consumer_key = os.environ.get('TWITTER_API_KEY')
consumer_secret = os.environ.get('TWITTER_API_KEY_SECRET')
key = os.environ.get('ACCESS_TOKEN')
secret = os.environ.get('ACCESS_TOKEN_SECRET')

# Create Twitter authorization instance
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
    
api = tweepy.API(auth)
api.update_status('tweepy + oauth!')


# Create Spotipy object based off of user ID
# stored in variable username.
spotifyObject = spotipy.Spotify(auth=token)

user = spotifyObject.current_user()
while(True):
    print()
    artistQuery = input("Enter an artist's name for 5 song recommendations: ") # Prompt user input
    artistID = spotifyObject.search(artistQuery,1,0,"artist") ['artists']['items'][0]['id']
    list = []
    list.append(artistID)
    print()
    trackList = spotifyObject.recommendations(list, None, None, 5, 'US') # Store 5 song recommendations
    print("Here are five recommended songs (in no particular order):\n")
    count = 0
    while (count < 5):
        trackName = trackList['tracks'][count]['name'] # Get track name
        artistName = trackList['tracks'][count]['artists'][0]['name'] # Get artist name
        print(count+1, ". " + trackName + " by " + artistName + "\n")
        count = count + 1
    userContinue = input("Would you like to search for another recommendation? (enter 'y' for yes. Any other key will end this program) ")
    if (userContinue.lower() != 'y'):
        break


# print(json.dumps(VARIABLE, sort_keys=True, indent=4))