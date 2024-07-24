# Xenia Canary Installer

This script simplifies the process of setting up Xenia Canary, a popular Xbox 360 emulator, by automating the download and extraction of the latest release and the necessary game patches.

## Features

- Downloads the latest release of Xenia Canary from GitHub.
- Extracts the downloaded zip file to a specified directory.
- Downloads the latest game patches from the Xenia Canary repository.
- Extracts the game patches and copies them to the Xenia Canary directory.
- Cleans up temporary files after extraction.

## Requirements

- Python 3.6 or higher
- `requests` library
- `zipfile` library
- `shutil` library
