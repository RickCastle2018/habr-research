import re
import requests as r
from fake_useragent import UserAgent
import json
import datetime


def news():

    # generating time-depending filename, so that the data is not overwritten when you run it again
    now = datetime.datetime.now()
    filename = "data" + str(now.minute) + str(now.second) + ".json"

    # habr "kek api v2" gives away articles in html
    def cleanhtml(raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext.replace("\r\n", "")

    # get_page gets news page in json
    def get_page(num):
        API_URL = 'https://m.habr.com/kek/v2/articles?fl=ru&hl=ru&news=true&page=%d' % (
            num)
        #added random-useragent
        response = r.get(API_URL, headers={'User-Agent': UserAgent().random})
        if response.status_code == 200:
            json = response.json()
            return json

    # full_text get full text of article (get_page gives just teaser)
    def full_text(id):
        API_URL = 'https://m.habr.com/kek/v2/articles/%d' % (id)
        response = r.get(API_URL)
        if response.status_code == 200:
            json = response.json()
            text = json['textHtml']
            return text

    # getting pages count to stop 'for' cycle
    pages = get_page(1)['pagesCount']

    # to have a valid json array
    with open(filename, 'a', encoding='utf-8') as f:
        f.write("[")

    # get and write in file all news
    count = 0
    for i in range(1, pages + 1):
        page = get_page(i)
        for ref in page['articleRefs'].values():
            piece_of_news = {}

            # collect data we need in piece_of_news
            piece_of_news['views'] = ref['statistics']['readingCount']
            piece_of_news['rating'] = ref['statistics']['score']
            piece_of_news['votes'] = ref['statistics']['votesCount']
            piece_of_news['favorites'] = ref['statistics']['favoritesCount']
            piece_of_news['comments'] = ref['statistics']['commentsCount']
            piece_of_news['pubdate'] = ref['timePublished']
            piece_of_news['teaser'] = cleanhtml(ref['leadData']['textHtml'])
            piece_of_news['header'] = cleanhtml(ref['titleHtml'])
            piece_of_news['text'] = cleanhtml(full_text(int(ref['id'])))

            # write piece_of_news into file
            with open(filename, 'a', encoding='utf-8') as f:
                json.dump(piece_of_news, f, ensure_ascii=False, indent=4)
                f.write(",")

            # to watch progress
            count = count + 1
            print(count)

    # to have a valid json array
    with open(filename, 'a', encoding='utf-8') as f:
        f.write("]")

    print('Data received. And Written.')


news()
