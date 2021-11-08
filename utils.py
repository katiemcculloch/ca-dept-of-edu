from bs4 import BeautifulSoup
import requests

def get_content_from_url(url):    
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')
