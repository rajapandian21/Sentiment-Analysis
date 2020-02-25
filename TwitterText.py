import tweepy as tw
import json
import pandas as pd


def pullTweets(hasTagWord, searchStartDate, maxNoOfTweets):
    print(hasTagWord, searchStartDate, maxNoOfTweets)
    print(type(maxNoOfTweets))
    print(type(searchStartDate))
    consumer_api_key = "3VbKOgmaGoh9lXqrfBWDRWIVH"
    consumer_api_secret_key = "k21iNXSwyDy628VG6J4Gieec91wyxAS5fG5fOohgSMn7OniYin"
    access_token = "4732473492-9VcLpbnxyRIWzGggwNXApcD4QIRf2bV1aCO2pwC"
    access_token_secret = "J6ZMnQ874dREaXadm2ksdLI9IHa4xoaCHe1Nghvf3C9Tf"

    auth = tw.OAuthHandler(consumer_api_key, consumer_api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    tweets = tw.Cursor(api.search,
                  q=hasTagWord,
                  lang="en",
                  since=searchStartDate, tweet_mode="extended").items(int(maxNoOfTweets))

    json_data = [r._json for r in tweets]
    df = pd.io.json.json_normalize(json_data)
    #df1 = df[['created_at', 'full_text', 'user.name', 'user.location', 'geo', 'coordinates', 'place' , 'lang']]
    text = df['full_text'].tolist()
    return text