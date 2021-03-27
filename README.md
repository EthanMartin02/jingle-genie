# Twitter Jingle Genie
---
## https://twitter.com/jingle_genie
### Twitter bot that generates a list of recommended tracks based off of user input of the name of an artist.
---
- This bot runs on an AWS Lambda function that polls every minute. (128 MB per execution with a 30 second timeout)
- Uses the official Spotify API to generate relevant music recommendations based off of what artist is input.
- This bot will tweet @ users that mention it with a list of recommended tracks
-- If the user submits an invalid input, this bot will respond with a request for another input that is valid.