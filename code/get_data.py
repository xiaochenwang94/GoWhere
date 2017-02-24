import tweepy

consumer_key = 'kfaj0I2197iZvXhcQUYdlGBwp'
consumer_secret = '3IST0USpxSKDOsqTnUlbC87x3mgdQResvaSWLWozdlka8VRCm7'
access_token = '709704756336308226-6eN5Avi0VzSb7WqRHso3Ayu2xKDXYdR'
access_secret = 'DRXzJD6IP2v1VhYRaGFpkUfL6WjE19AL60HRW3D7mQW4h'

auth  = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)
api = tweepy.API(auth)
public_tweets = api.search('Trump')

for tweet in public_tweets:
    print(tweet.text)

