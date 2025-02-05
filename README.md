# Twitter Data Scraper

[![Promo](https://github.com/luminati-io/LinkedIn-Scraper/raw/main/Proxies%20and%20scrapers%20GitHub%20bonus%20banner.png)](https://brightdata.com/products/web-scraper/twitter)

This repository provides two distinct methods for collecting Twitter data:
1. **Free Twitter Scraper**: For small-scale projects and learning
2. [**Enterprise Twitter Scraper API**](https://brightdata.com/products/web-scraper/twitter): For production-grade data extraction

## Table of Contents
1. [Free Twitter Scraper](#free-twitter-scraper)
    - [Profile Scraping](#1-profile-scraping)
    - [Post Scraping](#2-post-scraping)
    - [Limitations](#limitations)
2. [Twitter Scraper API](#twitter-scraper-api)
    - [Key Features](#key-features)
    - [Quick Start Guide](#quick-start-guide)
    - [Scrape Posts by URL](#1-scrape-posts-by-url)
    - [Scrape Profile Data](#2-scrape-profile-data)
    - [Date-Range Tweet Collection](#3-date-range-tweet-collection)
3. [No-Code Scraper Option](#no-code-scraper-option)
4. [Data Collection Approaches](#data-collection-approaches)
5. [Support & Resources](#support--resources)


## Free Twitter Scraper
Ideal for small-scale projects, experiments, and learning purposes.

### 1. Profile Scraping
Extracts public profile data from Twitter, including names, followers, tweet counts, and more.

#### Input Requirements:
| Parameter  | Type  | Required | Description                          |
|------------|-------|----------|--------------------------------------|
| usernames  | list  | Yes      | List of Twitter handles to scrape   |

#### Implementation:
```python
# free_scraper/twitter_profiles.py
usernames = [
    "satyanadella",
    "BillGates", 
    "elonmusk"
]
```

#### Sample Output (CSV):
<img width="700" alt="twitter_profiles_data" src="https://github.com/luminati-io/twitter-scraper/blob/main/Images/408877618-450d920a-4760-463b-9670-8ac1264b6409.png" />

### 2. Post Scraping
Collect engagement metrics for specific tweets

#### Input Requirements:

| Parameter  | Type  | Required | Description                        |
|------------|-------|----------|------------------------------------|
| tweet_ids  | list  | Yes      | List of Twitter post IDs to scrape |

#### Implementation:
```python
# free_scraper/twitter_posts.py
TWEET_IDS = [
    "1882412972414214544",
    "1879604491764297992",
    "1869427646368792599"
]
```

#### Sample Output (JSON):
```json
{
  "tweet_id": "1882412972414214544",
  "author": "MongoDB",
  "content": "We're excited to announce...",
  "engagement": {
    "likes": 29,
    "retweets": 10,
    "views": 3417
  }
}
```

### Limitations
The free method is not recommended for large-scale scraping due to Twitter’s strict anti-bot protections. Some key limitations include:
- **Rate Limiting:** Twitter blocks requests after a few scrapes.
- **IP Blocking:** Frequent scraping from the same IP can lead to bans.
- **Limited Scalability:** Not suitable for high-volume data collection.
- **Restricted Data Fields:** Only provides basic profile and tweet data, with no advanced filtering options.

## Twitter Scraper API
A robust, scalable, and reliable solution for large-scale Twitter data extraction. Designed for businesses and developers who need high-quality, real-time data without infrastructure headaches.

### Key Features
- **Scalable & Reliable:** Optimized for high-volume and real-time data collection
- **Anti-Blocking:** Built-in [proxy rotation](https://brightdata.com/solutions/rotating-proxies) and [CAPTCHA solving](https://brightdata.com/products/web-unlocker/captcha-solver)
- **Legal Compliance:** Fully GDPR and CCPA compliant
- **Global Coverage:** Access data from any region or language
- **Real-Time Data:** Fresh data with minimal latency
- **Advanced Filtering:** Customize data extraction with precise filters
- **Pay-as-You-Go:** Only pay for successful responses
- **Free Trial:** Includes 20 free API calls to get started
- **Dedicated Support:** 24/7 technical assistance

👉 **Learn more:** [Bright Data Twitter Scraper API](https://brightdata.com/products/web-scraper/twitter)

### Quick Start Guide
- **Sign Up:** Create a [Bright Data account](https://brightdata.com/)
- **Get API Token:** Obtain your [API key](https://docs.brightdata.com/general/account/api-token) from the dashboard
- **Choose Endpoint:** Select from the available API endpoints below

### 1. Scrape Posts by URL
Extract detailed engagement metrics and content for specific tweets using their URLs.

<img width="700" alt="twitter-posts-scraper" src="https://github.com/luminati-io/twitter-scraper/blob/main/Images/409213804-9d07a475-2e3b-45fc-ae8e-ebcd7cef367b.png" />


#### Request Parameters:
| Field | Type   | Required | Description            |
|-------|--------|----------|------------------------|
| `url`   | string | Yes      | Full Twitter post URL |

#### Example Request:
```python
# twitter_api/twitter_posts.py
posts = [
    {"url": "https://x.com/OpenAI/status/1885406586136383634"},
    {"url": "https://x.com/CNN/status/1796673270344810776"}
]
```

#### Response Schema:
```json
{
    "post": {
        "author": {
            "name": "OpenAI",
            "followers": 3930255,
            "profileImage": "https://pbs.twimg.com/profile_images/1885410181409820672/ztsaR0JW_normal.jpg",
            "bio": "OpenAI's mission is to ensure that artificial general intelligence benefits all of humanity. We're hiring: https://t.co/dJGr6Lg202",
        },
        "content": {
            "text": "OpenAI o3-mini is now available in ChatGPT and the API.\n\nPro users will have unlimited access to o3-mini and Plus & Team users will have triple the rate limits (vs o1-mini).\n\nFree users can try o3-mini in ChatGPT by selecting the Reason button under the message composer.",
            "postedAt": "2025-01-31T19:15:33.000Z",
            "id": "1885406586136383634",
        },
        "engagement": {
            "replies": 1004,
            "reposts": 1997,
            "likes": 13420,
            "views": 2858777,
            "quotes": 684,
            "bookmarks": 1546,
        },
    }
}
```
👉 Only key fields are shown here. See the [full JSON response](https://github.com/luminati-io/Twitter-Scraper/blob/main/twitter_data/twitter_posts.json) for all details.

### 2. Scrape Profile Data
Extract comprehensive profile information, including recent posts and engagement metrics.

<img width="600" alt="twitter-profile-scraper" src="https://github.com/luminati-io/twitter-scraper/blob/main/Images/409214197-3b3e2f0f-30bc-45d9-b9bc-13358b22a55a.png" />

#### Request Parameters:

| Field      | Type   | Required | Description                     |
|------------|--------|----------|---------------------------------|
| `url`        | string | Yes      | Twitter profile URL       |
| `max_number_of_posts`  | number | No       | Number of recent posts to retrieve |

#### Example Request:
```python
# twitter_api/twitter_profile_posts.py
profiles = [
    {"url": "https://x.com/satyanadella", "max_number_of_posts": 50},
    {"url": "https://x.com/BillGates", "max_number_of_posts": 35}
]
```

#### Response Schema:
```json
{
    "profile": {
        "name": "Satya Nadella",
        "handle": "satyanadella",
        "role": "Chairman and CEO at Microsoft",
        "isVerified": true,
        "profileImage": "https://pbs.twimg.com/profile_images/1221837516816306177/_Ld4un5A_normal.jpg",
        "website": "http://www.microsoft.com/ceo",
        "joinedDate": "2009-02-11T04:45:34.000Z",
        "stats": {"following": 286, "followers": 3356268, "postsCount": 1859},
    },
    "posts": [
        {
            "id": "1807114709499523208",
            "content": "What a final!!! Congrats, India, and well played, South Africa. Super World Cup... let us have more cricket in the West Indies and USA!!",
            "postedAt": "2024-06-29T18:11:35.000Z",
            "engagement": {
                "replies": 712,
                "reposts": 10785,
                "likes": 133591,
                "views": 2029775,
            },
        },
        {
            "id": "1726509045803336122",
            "content": "We remain committed to our partnership with OpenAI and have confidence in our product roadmap, our ability to continue to innovate with everything we announced at Microsoft Ignite, and in continuing to support our customers and partners. We look forward to getting to know Emmett",
            "postedAt": "2023-11-20T07:53:28.000Z",
            "engagement": {
                "replies": 4524,
                "reposts": 14480,
                "likes": 89773,
                "views": 41675720,
            }
        },
    ],
}
```
👉 Only key fields are shown here. See the [full JSON response](https://github.com/luminati-io/Twitter-Scraper/blob/main/twitter_data/twitter_profile_posts.json) for all details.

### 3. Date-Range Tweet Collection
Retrieve posts within a specific date range.

#### Request Parameters:

| Parameter  | Type   | Required | Description                   |
|------------|--------|----------|-------------------------------|
| `url`        | string | Yes      | Twitter Profile URL          |
| `start_date` | string | Yes      | Start date (ISO format)       |
| `end_date`   | string | Yes      | End date (ISO format)         |


#### Example Request:
```python
# twitter_api/twitter_posts_date_range.py
profiles = [
    {
        "url": "https://x.com/satyanadella",
        "start_date": "2025-01-15T09:00:00.000Z",
        "end_date": "2025-01-31T23:00:00.000Z",
    },
    {"url": "https://x.com/cnn", "start_date": "2025-01-01", "end_date": "2025-01-15"},
    {"url": "https://x.com/fabrizioromano", "start_date": "", "end_date": ""},
]
```

#### Response Schema:
```json
{
    "post": {
        "author": {
            "name": "Satya Nadella",
            "handle": "satyanadella",
            "role": "Chairman and CEO at Microsoft",
            "isVerified": false,
            "profileImage": "https://pbs.twimg.com/profile_images/1221837516816306177/_Ld4un5A_normal.jpg",
            "followers": 3356282,
            "following": 286,
        },
        "content": {
            "text": "For me, cricket is maybe the only thing that could possibly come close to watching the Excel World Champ on ESPN!",
            "images": ["https://pbs.twimg.com/media/GiF4nePaEAAHQg5.jpg"],
            "externalUrl": "https://techcommunity.microsoft.com/blog/excelblog/congrats-to-the-winners-of-this-years-mewc--mecc/4355651",
            "postedAt": "2025-01-24T22:29:46.000Z",
            "id": "1882918743409676719",
        },
        "engagement": {
            "replies": 102,
            "reposts": 208,
            "likes": 3416,
            "views": 286901,
            "quotes": 39,
            "bookmarks": 127,
        },
    }
}
```
👉 Only key fields are shown here. See the [full JSON response](https://github.com/luminati-io/Twitter-Scraper/blob/main/twitter_data/twitter_date_range_posts.json) for all details.

## No-Code Scraper Option
For users preferring a graphical interface, we offer a no-code solution through our control panel:

- Configure scrapers in minutes
- Automates the entire data collection process
- Direct result download (multiple formats)

For detailed instructions on using the no-code scraper, please visit our [Getting Started guide](https://github.com/luminati-io/Twitter-Scraper/blob/main/no-code-scraper.md).


## Data Collection Approaches
You can use the following parameters to fine-tune your results:
| **Parameter**       | **Type**   | **Description**                                            | **Example**                  |
|---------------------|------------|------------------------------------------------------------|------------------------------|
| `limit`             | `integer`  | Max results per input                                   | `limit=10`                   |
| `include_errors`    | `boolean`  | Get error reports for troubleshooting                     | `include_errors=true`        |
| `notify`            | `url`      | Webhook notification URL to be notified upon completion  | `notify=https://notify-me.com/` |
| `format`            | `enum`     | Output format (e.g., JSON, NDJSON, JSONL, CSV)         | `format=json`                |

💡 **Pro Tip:** You can also select whether to deliver the data to an [external storage](https://docs.brightdata.com/scraping-automation/web-data-apis/web-scraper-api/overview#via-deliver-to-external-storage) or to deliver it to a [webhook](https://docs.brightdata.com/scraping-automation/web-data-apis/web-scraper-api/overview#via-webhook).

## Support & Resources
- **API Documentation:** [Bright Data Docs](https://docs.brightdata.com/scraping-automation/web-scraper-api/trigger-a-collection)
- **Scraping Best Practices:** [Avoid Getting Blocked](https://brightdata.com/blog/web-data/web-scraping-without-getting-blocked)
- **Technical Support:** [Contact Us](mailto:support@brightdata.com)

---

**Interested in other scrapers? Check out the list below:**

- [LinkedIn Scraper](https://github.com/luminati-io/LinkedIn-Scraper)
- [Google News Scraper](https://github.com/luminati-io/Google-News-Scraper)
- [Google Maps Scraper](https://github.com/luminati-io/Google-Maps-Scraper)
- [Amazon Scraper](https://github.com/luminati-io/Amazon-scraper)
