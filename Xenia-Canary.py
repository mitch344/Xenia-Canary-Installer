import requests
import os
import zipfile
import shutil

def get_latest_release(repo):
    url = f'https://api.github.com/repos/{repo}/releases/latest'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def download_asset(asset_url, destination):
    headers = {'Accept': 'application/octet-stream'}
    response = requests.get(asset_url, headers=headers, stream=True)
    response.raise_for_status()

    with open(destination, 'wb') as out_file:
        for chunk in response.iter_content(chunk_size=8192):
            out_file.write(chunk)

def download_zip_from_github(repo, branch, destination):
    url = f'https://github.com/{repo}/archive/refs/heads/{branch}.zip'
    headers = {'Accept': 'application/octet-stream'}
    response = requests.get(url, headers=headers, stream=True)
    response.raise_for_status()

    with open(destination, 'wb') as out_file:
        for chunk in response.iter_content(chunk_size=8192):
            out_file.write(chunk)

def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        print(f"Extracted to {extract_to}.")

def copy_patches_to_xenia_canary():
    source_patches = os.path.join("game-patches", "game-patches-main", "patches")
    dest_xenia_canary = "xenia_canary"
    
    if os.path.exists(source_patches):
        shutil.copytree(source_patches, os.path.join(dest_xenia_canary, "patches"))
        print(f"Copied patches to {dest_xenia_canary}")
        shutil.rmtree("game-patches")
        print("Deleted game-patches directory and all its contents.")
    else:
        print("Patches directory not found!")

def main():
    xenia_canary_repo = "xenia-canary/xenia-canary"
    asset_name = "xenia_canary.zip"
    xenia_destination = "xenia_canary.zip"
    xenia_extract_dir = "xenia_canary"

    release = get_latest_release(xenia_canary_repo)
    asset = next((a for a in release['assets'] if a['name'] == asset_name), None)

    if asset:
        print(f"Downloading {asset['name']}...")
        download_asset(asset['browser_download_url'], xenia_destination)
        print(f"Downloaded to {xenia_destination}.")
        print(f"Extracting {xenia_destination} to {xenia_extract_dir}...")
        extract_zip(xenia_destination, xenia_extract_dir)
        print(f"Deleting {xenia_destination}...")
        os.remove(xenia_destination)
        print(f"{xenia_destination} deleted.")
    else:
        print(f"No asset named {asset_name} found in the latest release.")

    game_patches_repo = "xenia-canary/game-patches"
    game_patches_destination = "game-patches.zip"
    game_patches_extract_dir = "game-patches"
    
    print(f"Downloading main branch of {game_patches_repo}...")
    download_zip_from_github(game_patches_repo, "main", game_patches_destination)
    print(f"Downloaded to {game_patches_destination}.")
    print(f"Extracting {game_patches_destination} to {game_patches_extract_dir}...")
    extract_zip(game_patches_destination, game_patches_extract_dir)
    print(f"Deleting {game_patches_destination}...")
    os.remove(game_patches_destination)
    print(f"{game_patches_destination} deleted.")
    copy_patches_to_xenia_canary()

if __name__ == '__main__':
    main()
