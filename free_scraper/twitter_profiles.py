import requests
import json
import csv
import time

# List of 10 usernames to query
usernames = [
    "satyanadella",
    "BillGates",
    "elonmusk",
    "tim_cook",
    "sundarpichai",
    "nasa",
    "neiltyson",
    "verge",
    "wired",
    "techcrunch",
]


def flatten_user_data(user_data):
    """Extract and flatten relevant user data from the JSON response."""
    legacy = user_data.get("legacy", {})
    verification_info = (
        user_data.get("verification_info", {})
        .get("reason", {})
        .get("description", {})
        .get("text", "N/A")
    )

    return {
        "user_id": user_data.get("rest_id", "N/A"),
        "screen_name": legacy.get("screen_name", "N/A"),
        "name": legacy.get("name", "N/A"),
        "followers_count": legacy.get("followers_count", 0),
        "following_count": legacy.get("friends_count", 0),
        "tweet_count": legacy.get("statuses_count", 0),
        "description": legacy.get("description", "N/A"),
        "verified": user_data.get("is_blue_verified", False),
        "created_at": legacy.get("created_at", "N/A"),
        "profile_image_url": legacy.get("profile_image_url_https", "N/A"),
        "affiliation": user_data.get("affiliates_highlighted_label", {})
        .get("label", {})
        .get("description", "N/A"),
        "verification_reason": verification_info,
        "location": legacy.get("location", "N/A"),
        "url": legacy.get("url", "N/A"),
    }


# CSV file setup
filename = "twitter_profiles.csv"
fieldnames = [
    "user_id",
    "screen_name",
    "name",
    "followers_count",
    "following_count",
    "tweet_count",
    "description",
    "verified",
    "created_at",
    "profile_image_url",
    "affiliation",
    "verification_reason",
    "location",
    "url",
]

# Cookies and headers for the request
cookies = {
    "d_prefs": "MjoxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw",
    "guest_id": "v1%3A173847241574643869",
    "night_mode": "2",
    "guest_id_marketing": "v1%3A173847241574643869",
    "guest_id_ads": "v1%3A173847241574643869",
    "att": "1-wEVBVhEvbjoeOxO6NcJUbAEuiotm5ZKsu8BeYxWC",
    "gt": "1886026951904682400",
    "personalization_id": '"v1_yLGh2phjsqHzxowhxjDLWg=="',
}

headers = {
    "accept": "*/*",
    "accept-language": "en-GB,en;q=0.5",
    "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    "content-type": "application/json",
    "origin": "https://x.com",
    "priority": "u=1, i",
    "referer": "https://x.com/",
    "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Brave";v="132"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "x-client-transaction-id": "xzBVx+UCZJL9WDDYHZXJ3y+bqfOeAxaxSIsNlt1BgZcadIPYnoVhWuzvQ70sIVbthCnFl8SiWeykMhZPadpsA8hKHL7CxA",
    "x-guest-token": "1886026951904682400",
    "x-twitter-active-user": "yes",
    "x-twitter-client-language": "en-GB",
}

# Common parameters for all requests
features = json.dumps(
    {
        "hidden_profile_subscriptions_enabled": True,
        "profile_label_improvements_pcf_label_in_post_enabled": True,
        "rweb_tipjar_consumption_enabled": True,
        "responsive_web_graphql_exclude_directive_enabled": True,
        "verified_phone_label_enabled": True,
        "subscriptions_verification_info_is_identity_verified_enabled": True,
        "subscriptions_verification_info_verified_since_enabled": True,
        "highlights_tweets_tab_ui_enabled": True,
        "responsive_web_twitter_article_notes_tab_enabled": True,
        "subscriptions_feature_can_gift_premium": True,
        "creator_subscriptions_tweet_preview_api_enabled": True,
        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
        "responsive_web_graphql_timeline_navigation_enabled": True,
    }
)

field_toggles = json.dumps({"withAuxiliaryUserLabels": False})

# Write data to CSV
with open(filename, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for username in usernames:
        try:
            params = {
                "variables": json.dumps({"screen_name": username}),
                "features": features,
                "fieldToggles": field_toggles,
            }

            response = requests.get(
                "https://api.x.com/graphql/32pL5BWe9WKeSK1MoPvFQQ/UserByScreenName",
                params=params,
                cookies=cookies,
                headers=headers,
            )

            if response.status_code == 200:
                data = response.json()
                if "data" in data and "user" in data["data"]:
                    user_data = data["data"]["user"]["result"]
                    flat_data = flatten_user_data(user_data)
                    writer.writerow(flat_data)
                    print(f"Successfully saved data for @{username}")
                else:
                    print(f"No data found for @{username} - might be private/suspended")
            else:
                print(f"Error for @{username}: {response.status_code}")

        except Exception as e:
            print(f"Exception occurred for @{username}: {str(e)}")

        # Add a delay between requests to avoid rate limiting
        time.sleep(1)

print(f"\nData collection complete! Saved to {filename}")
