import requests
import os
from urllib.parse import urlparse
from hashlib import md5

def fetch_image(url, save_dir="Fetched_Images"):
    """
    Fetch an image from the given URL and save it to the specified directory.
    Handles HTTP errors, prevents duplicates, and creates the directory if needed.
    """
    try:
        # Ensure the directory exists
        os.makedirs(save_dir, exist_ok=True)

        # Fetch image with headers
        headers = {"User-Agent": "UbuntuImageFetcher/1.0 (meseretakalu)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise error for bad HTTP responses

        # Ensure the content is an image
        if "image" not in response.headers.get("Content-Type", ""):
            print(f"✗ Skipping URL (not an image): {url}")
            return

        # Extract filename or generate one using hash
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = md5(response.content).hexdigest() + ".jpg"

        filepath = os.path.join(save_dir, filename)

        # Avoid duplicate files
        if os.path.exists(filepath):
            print(f"⚠️ Duplicate detected, skipping: {filename}")
            return

        # Save image
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ An error occurred: {e}")


def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    urls_input = input("Please enter image URL(s) (comma-separated for multiple): ")
    urls = [url.strip() for url in urls_input.split(",")]

    for url in urls:
        fetch_image(url)

    print("\nConnection strengthened. Community enriched.")


if __name__ == "__main__":
    main()
