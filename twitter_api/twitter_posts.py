import requests
import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")


class TwitterPostsCollector:
    API_BASE_URL = "https://api.brightdata.com/datasets/v3"
    DATASET_ID = "gd_lwxkxvnf1cynvib9co"

    def __init__(self, api_token: str):
        """Initialize the collector with API token and request headers."""
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }

    def collect_posts(self, post_urls: List[Dict[str, str]]) -> Optional[bool]:
        """Trigger data collection, monitor status, and save the results."""
        start_time = datetime.now()
        print(f"\nStarting collection for {len(post_urls)} posts...")

        collection_response = self._trigger_collection(post_urls)
        if not collection_response or "snapshot_id" not in collection_response:
            logging.error("Failed to initiate data collection")
            return None

        snapshot_id = collection_response["snapshot_id"]
        last_status = None

        while True:
            status = self._check_status(snapshot_id)
            elapsed = (datetime.now() - start_time).seconds

            if status != last_status:
                if status == "running":
                    print(f"Collection in progress... ({elapsed}s elapsed)")
                elif status == "ready":
                    print(f"Collection completed in {elapsed} seconds")
                elif status in ["failed", "error"]:
                    print(f"Collection failed after {elapsed} seconds")
                    return None
                last_status = status

            if status == "ready":
                posts_data = self._fetch_data(snapshot_id)
                if posts_data:
                    break
            elif status in ["failed", "error"]:
                return None

            time.sleep(5)

        self._save_data(posts_data)
        print("Data saved successfully\n")
        return True

    def _trigger_collection(self, post_urls: List[Dict[str, str]]) -> Optional[Dict[str, Any]]:
        """Send a request to initiate data collection for given Twitter post URLs."""
        try:
            response = requests.post(
                f"{self.API_BASE_URL}/trigger",
                headers=self.headers,
                params={"dataset_id": self.DATASET_ID, "include_errors": "true"},
                json=post_urls,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"API error: {str(e)}")
            return None

    def _check_status(self, snapshot_id: str) -> Optional[str]:
        """Check the current status of the data collection process."""
        try:
            response = requests.get(
                f"{self.API_BASE_URL}/progress/{snapshot_id}",
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()
            return response.json().get("status")
        except requests.exceptions.RequestException:
            return "error"

    def _fetch_data(self, snapshot_id: str) -> Optional[List[Dict[str, Any]]]:
        """Retrieve collected data once the snapshot is ready."""
        try:
            response = requests.get(
                f"{self.API_BASE_URL}/snapshot/{snapshot_id}",
                headers=self.headers,
                params={"format": "json"},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None

    def _save_data(self, data: List[Dict[str, Any]], filename: str = "twitter_posts.json") -> None:
        """Save the collected data to a JSON file."""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Error saving data: {str(e)}")


def main() -> None:
    """Run the Twitter post collection process with sample URLs."""
    api_token = "YOUR_API_TOKEN"
    collector = TwitterPostsCollector(api_token)

    posts = [
        {"url": "https://x.com/OpenAI/status/1885406586136383634"},
        {"url": "https://x.com/FabrizioRomano/status/1552015619251634176"},
        {"url": "https://x.com/FabrizioRomano/status/1665296716721946625"},
        {"url": "https://x.com/CNN/status/1796673270344810776"}
    ]

    collector.collect_posts(posts)


if __name__ == "__main__":
    main()