import requests
from bs4 import BeautifulSoup


def getNews(lang):
    newsList = []
    newsEnList = []
    googleNews = "news.google.com"
    url = "https://news.google.com/?hl=" + lang + "-IN&gl=IN&ceid=IN:"+lang
    if googleNews in url:
        result = requests.get(url)
        if result.status_code == 200:
            src = result.content
            soup = BeautifulSoup(src, 'lxml')
            links = soup.find_all(["h3","h4"])
            for link in links:
                if link.find('a'):
                    aLink = link.find('a')
                    if len(aLink.text) > 0:
                        newsList.append(aLink.text)

        else:
            print('Page is unavailabe')
    else:
        print('Invalid URL')

    newsEnList = newsList
    if lang != 'en':
        from googletrans import Translator
        translator = Translator()
        newsEnList = translator.translate(newsList)
        newsEnList = [x.text for x in newsEnList]
    return newsList, newsEnList
