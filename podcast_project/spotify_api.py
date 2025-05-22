import requests
import base64
import re

# Your Spotify Developer Account Information
client_id = '6fb7e1766693439b86ec57e3deb3c36f'
client_secret = 'da3f94c6a68d49f6b64a7216ec9eb905'

# Remove "Firstory Hosting"
def clean_description(desc):
    return re.sub(r'Powered by Firstory Hosting.*$', '', desc).strip()

# Get access token
def get_access_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()
    }
    data = {
        'grant_type': 'client_credentials'
    }

    response = requests.post(auth_url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()['access_token']

# Search for Podcasts (shows) using a keyword
def search_podcast(keyword, token, limit=5):
    search_url = 'https://api.spotify.com/v1/search'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = {
        'q': keyword,
        'type': 'show',  # Specify search type as podcast
        'limit': limit
    }

    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    results = response.json()
    print(results)
    for idx, show in enumerate(results['shows']['items'], 1):
        description = clean_description(show['description'])
        print(f"{idx}. Name: {show['name']}")
        print(f"   Publisher: {show['publisher']}")
        print(f"   Description: {description}")
        print(f"   Spotify Link: {show['external_urls']['spotify']}")
        print()

# Main program
if __name__ == '__main__':
    token = get_access_token(client_id, client_secret)
    keyword = 'Finance'  # The keyword you want to search for
    search_podcast(keyword, token)
