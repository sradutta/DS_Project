import tweepy
import csv

CONSUMER_KEY = 'MExajNuZUYOj61FKHxGqhM50P'
CONSUMER_SECRET = 'l03vdCZQ8cC98OIOPNdJt22vX7bEVQLH2YChneFiiQg6mG1yrO'
OAUTH_TOKEN = '2575701463-qznBt6icVJuxOLseAkH22ko66IZOrO3KbDihO9T'
OAUTH_TOKEN_SECRET = 'A4nV7KCst5dXaHuP4KZGhQSmYdvxOfqkznwTyTc5Y4QJC'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = tweepy.API(auth)
csvFile = open('result.csv', 'a')
csvWriter = csv.writer(csvFile)

for tweet in tweepy.Cursor(api.search, q="google", since="2014-02-14", until="2014-02-15", lang="en").items():
	csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
	print tweet.created_at, tweet.text
csvFile.close()

