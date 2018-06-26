from secrets import Oauth_Secrets
import tweepy
from textblob import TextBlob


def primary(hashtag):
    secrets = Oauth_Secrets()
    auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
    auth.set_access_token(secrets.access_token, secrets.access_token_secret)

    api = tweepy.API(auth)

    N = 100
    tweets = tweepy.Cursor(api.search, q=hashtag).items(N)
    neg = 0.0
    pos = 0.0
    neg_count = 0
    pos_count = 0
    neutral_count = 0
    for tweet in tweets:
        blob = TextBlob(tweet.text)
        if blob.sentiment.polarity < 0:
            neg += blob.sentiment.polarity
            neg_count += 1
        elif blob.sentiment.polarity > 0:
            pos += blob.sentiment.polarity
            pos_count += 1
        else:
            neutral_count += 1

    return [['Sentiment', 'no of tweets'], ['Positive', pos_count],
            ['Negative', neg_count], ['Neutral', neutral_count]]
