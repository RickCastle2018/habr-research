import re
import requests as r

# getting all news inarray

def news():

    def cleanhtml(raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    def get_page(num):
        API_URL = 'https://m.habr.com/kek/v2/articles?fl=ru&hl=ru&news=true&page=%d' % (num)
        response = r.get(API_URL)
        if response.status_code == 200:
            json = response.json()
            return json

    def full_text(id):
        API_URL = 'https://m.habr.com/kek/v2/articles/%d' % (id)
        response = r.get(API_URL)
        if response.status_code == 200:
            json = response.json()
            text = json['textHtml']
            return text

    pages = get_page(1)['pagesCount']

    news = []

    count = 0
    for i in range(1, pages + 1):
        page = get_page(i)
        for ref in page['articleRefs'].values():
            piece_of_news = {}

            piece_of_news['views'] = ref['statistics']['readingCount']
            piece_of_news['rating'] = ref['statistics']['score']
            piece_of_news['votes'] = ref['statistics']['votesCount']
            piece_of_news['favorites'] = ref['statistics']['favoritesCount']
            piece_of_news['comments'] = ref['statistics']['commentsCount']
            piece_of_news['pubdate'] = ref['timePublished']
            piece_of_news['teaser'] = cleanhtml(ref['leadData']['textHtml'])
            piece_of_news['header'] = cleanhtml(ref['titleHtml'])
            piece_of_news['text'] = cleanhtml(full_text(int(ref['id'])))

            news.append(piece_of_news)
            count = count + 1
            print(count)

    print('Data received.')

    return news