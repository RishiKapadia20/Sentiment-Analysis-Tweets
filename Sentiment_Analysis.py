#!/usr/bin/env python3

import tweepy
import csv
import os
from textblob import TextBlob

def Auth():
    consumer_key = '<consumer_key>'
    consumer_secret = '<consumer_secret>'

    access_token = '<access_token>'
    access_token_secret = '<access_token_secret>'

    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token, access_token_secret)


    api = tweepy.API(auth)



    return api

def tweetSearch(query, limit, language, api):
    data = dict()
    i = 0

    # public_tweets = api.search(q=[query], count=limit, language = language, tweet_mode = 'extended')
    public_tweets = tweepy.Cursor(api.search, q=query, lang=language,
                                  tweet_mode = 'extended').items(limit)


    for tweet in public_tweets:

        if "RT" in tweet.full_text:
            tweet_text = tweet.retweeted_status.full_text
        else:
            tweet_text = tweet.full_text

        analysis = TextBlob(tweet_text)
        data[i] = {"timestamp": tweet.created_at, "tweet": tweet_text.encode('utf-8'),
                   "polarity" : analysis.sentiment.polarity,
                    "subjectivity" : analysis.sentiment.subjectivity}
        i += 1

    return data

def dic_to_csv(file_location, csv_columns, dictionary):
    with open(file_location, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()

        for i in dictionary:
            writer.writerow(dictionary[i])


def main():
    api = Auth()
    data = tweetSearch("Trump",100,"en",api)
    
    csv_file = "tweet.csv"
    csv_columns = ['timestamp',	'tweet'	, 'polarity', 'subjectivity']

    dic_to_csv(csv_file, csv_columns, data)

if __name__ == "__main__":
    main()
