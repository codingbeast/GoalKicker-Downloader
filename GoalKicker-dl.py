import requests
from tqdm import tqdm
import os
import platform
import subprocess
import sys
from bs4 import BeautifulSoup
url = "https://goalkicker.com/"
downloadLocation = "GoalKicker Books"

# File Exists

def download_pdf_with_progress(url, output_path):
    try:
        # Send a GET request to the URL
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        
        # Get the total file size from the response headers
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # Block size for tqdm
        
        # Initialize progress bar
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading', ascii=True)

        with open(output_path, 'wb') as file:
            for data in response.iter_content(block_size):
                file.write(data)
                progress_bar.update(len(data))
        
        progress_bar.close()
        print(f"File downloaded successfully to: {output_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

def resourceExists(bookName, bookLink):
    if not os.path.exists(downloadLocation):
        os.mkdir(downloadLocation)
    if bookName:
        if os.path.isfile(f"{downloadLocation}/{bookName}.pdf"):
            return
        else:
            try:
                print("Downloading...")
                download_pdf_with_progress(bookLink, f"{downloadLocation}/{bookName}.pdf")

            except Exception:
                print("Couldn't download the resource file")

# Clear Screen


def clearScreen():
    if platform.system() == "Windows":
        subprocess.call("cls", shell=True)
    else:
        subprocess.call('clear', shell=True)
    return


# Main Logic

try:
    response = requests.get(url)
    print(response)

    # Extracting Homepage
    print("Extracting Homepage...")
    page = BeautifulSoup(response.text, 'html.parser')
    # Getting Books Page
    print("Extracting All the books from the homepage")
    booksDiv = page.findAll('div', {'class': 'bookContainer'})

    for bookDiv in booksDiv:
        bookName = bookDiv.text.replace('Â®', '')
        print(f"Getting:{bookName}")
        bookSlug = bookDiv.find('a').get('href')
        bookPageLink = requests.get(f"{url}{bookSlug}")
        bookPage = BeautifulSoup(bookPageLink.text, 'html.parser')
        bookLink = bookPage.find('button', {'class': 'download'}).get(
            'onclick').replace("'", '').replace('location.href=', f'{url}{bookSlug}')
        resourceExists(bookName, bookLink)
        clearScreen()
except KeyboardInterrupt:
    print("Interrepted by User!")
    sys.exit(0)
