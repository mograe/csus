import requests
from bs4 import BeautifulSoup

def random_pic():
    URL = "https://safebooru.org/index.php?page=post&s=random"
    raw = requests.get(URL).text
    soup = BeautifulSoup(raw, "html.parser")
    img = soup.find(id='image')
    return img['src']