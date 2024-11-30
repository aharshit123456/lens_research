import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from googleapiclient.discovery import build
import csv

def create_folder(keyword):
    folder_name = keyword.replace(" ", "_")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

def download_images(image_links, folder_name):
    for i, link in enumerate(image_links):
        try:
            response = requests.get(link, stream=True, timeout=10)
            response.raise_for_status()
            
            try:
                img = Image.open(BytesIO(response.content))
                img.verify()
                img = Image.open(BytesIO(response.content))
                valid_path = os.path.join(folder_name, f"image_{i + 1}.{img.format.lower()}")
                img.save(valid_path)
                print(f"Saved valid image: {valid_path}")
            except (UnidentifiedImageError, IOError):
                img = Image.open(BytesIO(response.content)).convert("RGB")
                valid_path = os.path.join(folder_name, f"image_{i + 1}.png")
                img.save(valid_path)
                print(f"Converted and saved invalid image: {valid_path}")
        
        except Exception as e:
            print(f"Failed to download {link}: {e}")

def search_images_api(keyword, num_results=10):
    api_key = "AIzaSyAIs7rS6azN9fzws-0PXMsSSUSdtk2lSww"
    cse_id = "97e5dab4880e147a2"

    service = build("customsearch", "v1", developerKey=api_key)
    try:
        results = service.cse().list(
            q=keyword,
            cx=cse_id,
            searchType="image",
            num=num_results
        ).execute()
        return [item["link"] for item in results.get("items", [])]
    except Exception as e:
        print(f"Error fetching images: {e}")
        return []

def save_to_csv(keyword, image_links):
    folder_name = keyword.replace(" ", "_")
    csv_file = f"{folder_name}.csv"
    data = [{"Image Link": link} for link in image_links]
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)
    print(f"CSV saved as {csv_file}")

def main():
    input_csv = "character_keywords.csv"
    with open(input_csv, 'r') as file:
        reader = csv.reader(file)
        keywords = [row[0] for row in reader]

    for keyword in keywords:
        print(f"Processing keyword: {keyword}")
        folder_name = create_folder(keyword)
        
        print("Searching for images...")
        searchterm = keyword + "cosplay"
        image_links = search_images_api(searchterm)
        print(f"Found {len(image_links)} images. Downloading...")
        
        download_images(image_links, folder_name)
        save_to_csv(keyword, image_links)
        print(f"Images saved in folder: {folder_name}")

if __name__ == "__main__":
    main()
