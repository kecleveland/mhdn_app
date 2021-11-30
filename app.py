from twarc import Twarc2, expansions
from pathlib import Path 
import json
import config
import os
import config

appConfig = config.Config
client = Twarc2(bearer_token=appConfig.bearer_token)
file_path = Path(f"{appConfig.file_path}{appConfig.file_name}")

def main():
    # result params 
    try:
        search_results = client.search_all(
                                    query=appConfig.query,
                                    start_time = appConfig.start_date,
                                    end_time = appConfig.end_date,
                                    max_results = appConfig.max_results
                                    )
    except Exception as e:
        print(f"An exception ocurred: {e}")

    # write results
    try:
        for page in search_results:
            result = expansions.flatten(page)
            # print(json.dumps(tweet))
            with open(file_path, "a+") as fh:
                for tweet in result:
                    fh.write("%s\n" % json.dumps(tweet))
    except IOError as e:
        print(f"Error: Issue writing to path {file_path}: {e}")
    else:
        print(f"Write to {file_path} successful.")

if __name__ == "__main__":
    main()