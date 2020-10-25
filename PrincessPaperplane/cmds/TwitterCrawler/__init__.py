import json
import requests
from queue import Queue


def fetch_tweets(name: str, bearer_token: str, queue: Queue):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream?expansions=attachments.media_keys,author_id&media.fields"
        "=preview_image_url,url&user.fields=id,profile_image_url,username",
        headers={"Authorization": "Bearer {}".format(bearer_token)}, stream=True
    )

    print(f"{name} status: {response.status_code}")
    if response.status_code == 200:
        for raw_tweet in response.iter_lines():
            if raw_tweet:
                queue.put(json.loads(str(raw_tweet, 'utf-8')))
