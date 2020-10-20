import re
import requests as r

# давай-ка кекнем все эти статьи!


def article(id):
    def cleanhtml(raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    def tags(value):
        array = []
        for tag in value:
            array.append(tag['titleHtml'])
        return array

    API_URL = 'https://m.habr.com/kek/v2/articles/%d/?fl=ru&hl=ru' % (id)
    article = {}

    response = r.get(API_URL)

    if response.status_code == 200:
        json = response.json()

        article['status'] = 'ok'
        article['title'] = cleanhtml(json['titleHtml'])
        article['text'] = cleanhtml(json['textHtml'])
        article['tags'] = tags(json['tags'])
        article['id'] = json['id']
        article['score'] = json['statistics']['score']
        article['votes'] = json['statistics']['votesCount']
        article['comments'] = json['statistics']['commentsCount']
        article['favorites'] = json['statistics']['favoritesCount']
    else:
        article['status'] = 'err'

    return article