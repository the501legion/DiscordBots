import json
import requests
from queue import Queue


def fetch_tweets(name: str, bearer_token: str, queue: Queue):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream",
        headers={"Authorization": "Bearer {}".format(bearer_token)}, stream=True
    )

    queue.put(f"[{name}] STATUS: {response.status_code}")
    if response.status_code == 200:
        for tweet in response.iter_lines():
            if tweet:
                elem = str(tweet).removeprefix('b')
                print(elem[1:len(elem) - 1])
                queue.put(f"[{name}]: {json.loads(elem[1:len(elem) - 1])['data']['text']}")
