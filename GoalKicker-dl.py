import requests
import os
import platform
import subprocess
import sys
from bs4 import BeautifulSoup
url = "https://goalkicker.com/"
downloadLocation = "GoalKicker Books"

# File Exists


def resourceExists(bookName, bookLink):
    if not os.path.exists(downloadLocation):
        os.mkdir(downloadLocation)
    if bookName:
        if os.path.isfile(f"{downloadLocation}/{bookName}.pdf"):
            return
        else:
            try:
                print("Downloading...")
                cmd = f'aria2c {bookLink} -c -o "{downloadLocation}/{bookName}.pdf"'
                subprocess.call(cmd, shell=True)

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
