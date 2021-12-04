import os
import config
from twarc import Twarc2, expansions
import pandas as pd
from pathlib import Path 
import json
import config
import time



appConfig = config.Config
client = Twarc2(bearer_token=appConfig.bearer_token)
file_path = Path(f"{appConfig.file_path}{appConfig.file_name}")

def main():
    # store results 
    all_tweets_list = []
    tweet_data_list = []
    user_information_dict = {}
    media_information_dict = {}

    try:
        search_results = client.search_all(
                                    query=appConfig.query,
                                    start_time = appConfig.start_date,
                                    end_time = appConfig.end_date,
                                    max_results = appConfig.max_results
                                )
        time.sleep(1) # need this because of limit (1 sec.)

        # write results
        for page in search_results:
            result = expansions.flatten(page)
            
            # print(json.dumps(tweet))
            with open(file_path, "a+") as fh:
                for tweet in result:
                    fh.write(f"Begin next dump:\n\n{json.dumps(tweet)}\n\n") 
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