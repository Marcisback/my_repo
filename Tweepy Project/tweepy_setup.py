import tweepy

BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAOsE3AEAAAAAFTdS4JDsRVyiPJDYYmrFbrbYix0%3D2970H5exG4NULOR6LFyfRR63BuV1mRFPzLLFBHA3RrVu0iPJer'
USERNAME = 'inbredsonly'

client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Search for recent tweets mentioning you
query = f'@{USERNAME} -from:{USERNAME}'
response = client.search_recent_tweets(
    query=query,
    tweet_fields=['author_id', 'referenced_tweets'],
    expansions=['author_id', 'referenced_tweets.id'],
    max_results=20
)

tweets = getattr(response, 'data', None)
if tweets:
    # Collect all replied_to tweet IDs
    replied_to_ids = []
    for tweet in tweets:
        referenced_tweets = getattr(tweet, 'referenced_tweets', None)
        if referenced_tweets:
            for ref in referenced_tweets:
                if getattr(ref, 'type', None) == 'replied_to':
                    replied_to_ids.append(ref.id)

    # Batch fetch original tweets (up to 100 at a time)
    if replied_to_ids:
        for i in range(0, len(replied_to_ids), 100):
            batch_ids = replied_to_ids[i:i+100]
            original_tweets_response = client.get_tweets(batch_ids, expansions=['author_id'])
            original_tweets = getattr(original_tweets_response, 'data', None)
            if original_tweets:
                for original_tweet in original_tweets:
                    original_author_id = getattr(original_tweet, 'author_id', None)
                    if original_author_id:
                        user_response = client.get_user(id=original_author_id)
                        user = getattr(user_response, 'data', None)
                        if user:
                            print(f"Original tweet author: @{getattr(user, 'username', 'unknown')}")
else:
    print("No such mentions found.")







