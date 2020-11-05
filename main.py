import KekApi as kek
import json

# pushing all news in data.json

if __name__ == "__main__":
    news = kek.news()

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(news, f, ensure_ascii=False, indent=4)

    print('Completed. Look for data.json file.')