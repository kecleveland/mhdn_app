import pandas as pd
pd.options.display.max_colwidth = 400
pd.options.display.max_columns = 90

test_tweets_df = pd.read_csv("twitter-data/02_test_tweet.csv",
                                parse_dates=["created_at"])

def make_tweet_url(tweets):
    username = tweets[0] #username
    tweet_id = tweets[1] #id
    tweet_url = f"https://twitter.com/{username}/status/{tweet_id}"
    return tweet_url

from ast import literal_eval 
def get_image_url(media):
    if type(media) != float and media != "{}":
        media = literal_eval(media)
        media = media[0]
        if "url" in media.keys():
            return media["url"]
    else:
        return "No Image URL"

test_tweets_df['tweet_url'] = test_tweets_df[['author.username', 'id']].apply(make_tweet_url, axis='columns')
test_tweets_df['media'] = test_tweets_df['attachments.media'].apply(get_image_url)

# rename columns in df
test_tweets_df.rename(columns={'created_at': 'date',
                          'public_metrics.retweet_count': 'retweets', 
                          'author.username': 'username', 
                          'author.name': 'name',
                          'public_metrics.like_count': 'likes', 
                          'public_metrics.quote_count': 'quotes', 
                          'public_metrics.reply_count': 'replies',
                          'author.description': 'user_bio'},
                            inplace=True)

# get custom data
tweets_df = test_tweets_df[['date', 'username', 'name', 'text', 'retweets',
           'likes', 'replies',  'quotes', 'tweet_url', 'media', 'user_bio']]


print(tweets_df)