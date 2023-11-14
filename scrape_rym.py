from playwright.sync_api import sync_playwright

from bs4 import BeautifulSoup

URL = "https://rateyourmusic.com/release/album"

artist = "radiohead"
album = "ok-computer"

# album_info_outer > album_info > tbody: get each tr in order: artist, type, released, recorded, rym ranking,

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page()
    page.goto(f"{URL}/{artist}/{album}")
    page.is_visible(".album_info_outer")
    html = page.inner_html(".album_info")

    print(html)

    soup = BeautifulSoup(html, "html.parser")

    print(soup.find_all("tr"))
