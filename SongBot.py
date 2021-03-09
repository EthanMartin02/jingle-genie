import os
import sys
import spotipy
import json
import spotipy.util as util
import random
import tweepy

# Sets up an Object that can interact with
# the Spotify API.
def spotifyAPISetup():
    username = os.environ.get('SPOTIPY_USERID')
    try:
        token = util.prompt_for_user_token(username)
    except:
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username)
    spotifyClient = spotipy.Spotify(auth=token)
    user = spotifyClient.current_user()
    return spotifyClient

# Sets up an Object that can interact with the
# Twitter API through a specific client account.
def twitterAPISetup():
    consumer_key = os.environ.get('TWITTER_API_KEY')
    consumer_secret = os.environ.get('TWITTER_API_KEY_SECRET')
    key = os.environ.get('ACCESS_TOKEN')
    secret = os.environ.get('ACCESS_TOKEN_SECRET')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)
    twitterClient = tweepy.API(auth)
    return twitterClient

# Returns a list of any new mentions that have not been
# replied to through the client Twitter account.
def getMentions(twitterClient):
    allMentions = twitterClient.mentions_timeline()
    currMentions = []
    if (len(allMentions) > 0):
        count = 0
        while (count < len(allMentions)) and (not allMentions[count].favorited):
            currMentions.insert(0, allMentions[count])
            count += 1
    return currMentions

# Creates and returns a list of the users
# that have mentioned the client Twitter account.
# Parameter mentions represents all the mentions
# that have not been replied to.
def getUsers(mentions):
    users = []
    for i in range(len(mentions)):
        nextUser = mentions[i].user.screen_name
        users.insert(0, nextUser)
    return users

# Creates and returns a list of all the recommendation
# requests that other Twitter users have made via mentions.
# Parameter mentions represents all the mentions that have
# not been replied to.
def getTweets(twitterClient, mentions):
    clientMention = "@" + twitterClient.me().screen_name
    tweets = []
    for i in range(len(mentions)):
        twitterClient.create_favorite(mentions[i].id)
        nextTweet = mentions[i].text.replace(clientMention, '')
        tweets.insert(0, nextTweet)
    return tweets

# Takes what the user requested and returns a string
# of recommendations if there is valid input.
# In the case of invalid inputs, the program will
# catch the error and return an error message.
def generateRecommendations(spotifyClient, user, tweet):
    NUM_RECOMMENDATIONS = 4
    result = "@" + user + ",\n"
    try:
        artistID = spotifyClient.search(tweet,1,0,"artist")['artists']['items'][0]['id']
    except:
        result += "Invalid input: please enter in the name of an artist!"
        return result
    list = []
    list.append(artistID)
    trackList = spotifyClient.recommendations(list, None, None, NUM_RECOMMENDATIONS, 'US') # Generate 4 song recommendations
    result += "Here are four recommended tracks for: \"" + tweet + "\"\n(in no particular order)\n"
    for i in range(NUM_RECOMMENDATIONS):
        trackName = trackList['tracks'][i]['name']
        artistName = trackList['tracks'][i]['artists'][0]['name']
        result += "\n" + str(i + 1) + ". " + trackName + " by " + artistName
    return result

# Main driver of the program
def main():
    spotifyClient = spotifyAPISetup()
    twitterClient = twitterAPISetup()
    mentions = getMentions(twitterClient)
    users = getUsers(mentions)
    tweets = getTweets(twitterClient, mentions)
    for i in range(len(mentions)):
        recommendation = generateRecommendations(spotifyClient, users[i], tweets[i])
        twitterClient.update_status(recommendation)

main()