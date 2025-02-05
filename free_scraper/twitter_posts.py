import requests
import json
from time import sleep
from typing import Optional, Dict, List

# Configuration
COOKIES = {
    "d_prefs": "MjoxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw",
    "guest_id": "v1%3A173847241574643869",
    "night_mode": "2",
    "guest_id_marketing": "v1%3A173847241574643869",
    "guest_id_ads": "v1%3A173847241574643869",
    "att": "1-wEVBVhEvbjoeOxO6NcJUbAEuiotm5ZKsu8BeYxWC",
    "gt": "1886026951904682400",
    "personalization_id": '"v1_cJUAgNXUvoHoFMsAKe3A0g=="',
}

HEADERS = {
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
    "x-client-transaction-id": "iEl80VZz0NJMYOy/rANcZzMNY5jHkotxm/y+lVqI6TcCRgtcDEvSEAzhwUTTzo18wKeA2IvstZMhbaLBQGCh4pMMrHvViw",
    "x-guest-token": "1886026951904682400",
    "x-twitter-active-user": "yes",
    "x-twitter-client-language": "en-GB",
}

FEATURES = {
    "creator_subscriptions_tweet_preview_api_enabled": True,
    "premium_content_api_read_enabled": False,
    "communities_web_enable_tweet_community_results_fetch": True,
    "c9s_tweet_anatomy_moderator_badge_enabled": True,
    "responsive_web_grok_analyze_button_fetch_trends_enabled": False,
    "responsive_web_grok_analyze_post_followups_enabled": False,
    "responsive_web_jetfuel_frame": False,
    "responsive_web_grok_share_attachment_enabled": True,
    "articles_preview_enabled": True,
    "responsive_web_edit_tweet_api_enabled": True,
    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
    "view_counts_everywhere_api_enabled": True,
    "longform_notetweets_consumption_enabled": True,
    "responsive_web_twitter_article_tweet_consumption_enabled": True,
    "tweet_awards_web_tipping_enabled": False,
    "responsive_web_grok_analysis_button_from_backend": True,
    "creator_subscriptions_quote_tweet_preview_enabled": False,
    "freedom_of_speech_not_reach_fetch_enabled": True,
    "standardized_nudges_misinfo": True,
    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
    "rweb_video_timestamps_enabled": True,
    "longform_notetweets_rich_text_read_enabled": True,
    "longform_notetweets_inline_media_enabled": True,
    "profile_label_improvements_pcf_label_in_post_enabled": True,
    "rweb_tipjar_consumption_enabled": True,
    "responsive_web_graphql_exclude_directive_enabled": True,
    "verified_phone_label_enabled": True,
    "responsive_web_grok_image_annotation_enabled": True,
    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
    "responsive_web_graphql_timeline_navigation_enabled": True,
    "responsive_web_enhance_cards_enabled": False,
}

TWEET_IDS = [
    "1882412972414214544",
    "1879604491764297992",
    "1869427646368792599",
    "1867608933176946806",
    "1885406586136383634",
]


def fetch_tweet_data(tweet_id: str) -> Optional[Dict]:
    """
    Fetch and extract essential data for a single tweet

    Args:
        tweet_id: The ID of the tweet to fetch

    Returns:
        Dict containing tweet data if successful, None otherwise
    """
    params = {
        "variables": json.dumps(
            {
                "tweetId": tweet_id,
                "withCommunity": False,
                "includePromotedContent": False,
                "withVoice": False,
            }
        ),
        "features": json.dumps(FEATURES),
        "fieldToggles": json.dumps(
            {
                "withArticleRichContentState": True,
                "withArticlePlainText": False,
                "withGrokAnalyze": False,
                "withDisallowedReplyControls": False,
            }
        ),
    }

    try:
        response = requests.get(
            "https://api.x.com/graphql/_y7SZqeOFfgEivILXIy3tQ/TweetResultByRestId",
            params=params,
            cookies=COOKIES,
            headers=HEADERS,
            timeout=10,
        )

        if response.status_code != 200:
            print(f"Error: Status code {response.status_code} for tweet {tweet_id}")
            return None

        data = response.json()
        result = data.get("data", {}).get("tweetResult", {}).get("result", {})

        if not result:
            print(f"No data found for tweet {tweet_id}")
            return None

        return {
            "tweet_id": tweet_id,
            "author": result.get("core", {})
            .get("user_results", {})
            .get("result", {})
            .get("legacy", {})
            .get("screen_name"),
            "verified": result.get("core", {})
            .get("user_results", {})
            .get("result", {})
            .get("is_blue_verified"),
            "content": result.get("legacy", {}).get("full_text"),
            "posted_at": result.get("legacy", {}).get("created_at"),
            "engagement": {
                "likes": result.get("legacy", {}).get("favorite_count"),
                "retweets": result.get("legacy", {}).get("retweet_count"),
                "views": result.get("views", {}).get("count"),
            },
        }

    except requests.exceptions.Timeout:
        print(f"Timeout while fetching tweet {tweet_id}")
    except requests.exceptions.RequestException as e:
        print(f"Network error while fetching tweet {tweet_id}: {str(e)}")
    except json.JSONDecodeError:
        print(f"Invalid JSON response for tweet {tweet_id}")
    except Exception as e:
        print(f"Unexpected error while fetching tweet {tweet_id}: {str(e)}")

    return None


def main():
    """Main function to fetch and save tweet data"""
    all_tweets: List[Dict] = []
    successful_fetches = 0

    for tweet_id in TWEET_IDS:
        print(f"Processing tweet {tweet_id}...")
        tweet_data = fetch_tweet_data(tweet_id)

        if tweet_data:
            all_tweets.append(tweet_data)
            successful_fetches += 1

        # Rate limiting protection
        sleep(1)

    # Save results
    if all_tweets:
        with open("twitter_posts.json", "w", encoding="utf-8") as f:
            json.dump(all_tweets, f, indent=2, ensure_ascii=False)
        print(f"Successfully saved {successful_fetches} tweets to twitter_posts.json")
    else:
        print("No tweets were successfully fetched")


if __name__ == "__main__":
    main()