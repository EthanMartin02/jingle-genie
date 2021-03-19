import os
import spotipy
import tweepy

# Sets up an Object that can interact with
# the Spotify API.
def spotifyAPISetup():
    username = os.environ.get('SPOTIPY_USERID')
    try:
        token = spotipy.util.prompt_for_user_token(username)
    except:
        os.remove(f".cache-{username}")
        token = spotipy.util.prompt_for_user_token(username)
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


# Takes what the user requested and returns a string
# of recommendations if there is valid input.
# In the case of invalid inputs, the program will
# catch the error and return an error message.
def generateRecommendations(spotifyClient, user, tweet, tweetID):
    NUM_RECOMMENDATIONS = 3
    result = "https://twitter.com/" + user
    result += "/status/" + str(tweetID) + "\n"
    try:
        artistID = spotifyClient.search(tweet,1,0,"artist")['artists']['items'][0]['id']
    except:
        result += "Invalid input: please enter in the name of an artist!"
        return result
    list = []
    list.append(artistID)
    trackList = spotifyClient.recommendations(list, None, None, NUM_RECOMMENDATIONS, 'US') # Generate 3 song recommendations
    result += "BOOM! Your wish has been granted.\n"
    result += "Here are " + str(NUM_RECOMMENDATIONS) + " recommended tracks for \"" + tweet + "\" (in no particular order):"
    for i in range(NUM_RECOMMENDATIONS):
        trackName = trackList['tracks'][i]['name']
        artistName = trackList['tracks'][i]['artists'][0]['name']
        result += "\n" + str(i + 1) + ". " + trackName + " by " + artistName
    return result

def lambda_handler(event, context):
    main()
    return

# Main driver of the program
def main():
    spotifyClient = spotifyAPISetup()
    twitterClient = twitterAPISetup()
    mentions = getMentions(twitterClient)
    clientMention = "@" + twitterClient.me().screen_name + " "
    for i in range(len(mentions)):
        recommendation = generateRecommendations(spotifyClient, mentions[i].user.screen_name,
            mentions[i].text.replace(clientMention, ''), mentions[i].id)
        tweet = twitterClient.update_status(recommendation)
        twitterClient.create_favorite(mentions[i].id)
        twitterClient.create_favorite(tweet.id)
        
main()