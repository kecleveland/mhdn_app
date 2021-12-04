from twarc import Twarc2, expansions
from pathlib import Path 
import tweepy
import time
import pandas as pd
import json
import config

appConfig = config.Config
# client = Twarc2(bearer_token=appConfig.bearer_token)
client = tweepy.Client(appConfig.bearer_token, wait_on_rate_limit=True)
file_path = Path(f"{appConfig.file_path}{appConfig.file_name}")
file_path_csv = Path(f"{appConfig.file_path}{appConfig.file_name_csv}")

""" def flatten_tweet(response_dict):
    for response in response_dict:
        for user in response.includes["users"]:
            pass """

def main():

    # result params 
    all_tweets_list = []
    # store results of each response
    tweet_data_list = []
    user_information_dict = {}
    media_information_dict = {}

    try:
        # get results
        for search_results in tweepy.Paginator(client.search_all_tweets,
                                            query=appConfig.query,
                                            user_fields = ["username", "description"],
                                            tweet_fields = ["public_metrics"],
                                            expansions = ["author_id"],
                                            media_fields = ["preview_image_url", "public_metrics"],
                                            start_time = appConfig.start_date,
                                            end_time = appConfig.end_date,
                                            max_results = appConfig.max_results):
            time.sleep(1) # need this because of limit (1 sec.)
            all_tweets_list.append(search_results)

 
        #loop through response
        for response in all_tweets_list:
            for user in response.includes["users"]:
                user_information_dict[user.id] = {"username": user.username,
                                                    "description": user.description,
                                                }
            
            for media in response.includes["media"]:
                media_information_dict[media.media_key] = {"media_url": media.preview_image_url}
                                               
            for tweet in response.data:
                #set author and tweet information
                author_info = user_information_dict[tweet.author_id]
                 # mapping 
                tweet_data_list.append({"author_id": tweet.author_id, 
                                        "username": author_info["username"],
                                        "text": tweet.text,
                                    })
       
        df = pd.DataFrame(tweet_data_list)
        print(df)
        df.to_csv(file_path_csv)
    except IOError as e:
        print(f"Error: Issue writing to path {file_path}: {e}")
    except ValueError as e:
        print(f"Failure flattening page: {e}")
    except Exception as e:
        print(f"An exception ocurred: {e}")
    else:
        print(f"Write to {file_path} successful.")

if __name__ == "__main__":
    main()