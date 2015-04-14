import pandas as pd

data_path = '/Users/kuttush/Desktop/Spongebob/Thinkful/DataScience/DS_Project/resultclimatecp.csv'
columns=['tweet-user-name', 'geo-location', 'profile-image-url', 'tweet-source', 'tweet-creation-time', 'tweet-text', 'retweet-count']
twitterdata1 = pd.read_csv(data_path, names=columns)

len(twitterdata1)
