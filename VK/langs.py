import requests
from bs4 import BeautifulSoup

def languages():
    langs = []
    # URL страницы с языками Google Translate
    url = "https://cloud.google.com/translate/docs/languages"
    
    # Выполняем GET-запрос
    response = requests.get(url)
    
    # Проверяем статус ответа
    if response.status_code != 200:
        print("Не удалось получить данные с сайта")
        return
    
    # Используем BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Находим таблицу с языками
    languages = {}
    for row in soup.select('table tbody tr'):
        cells = row.find_all('td')
        if len(cells) >= 2:
            lang_code = cells[0].text.strip()
            lang_name = cells[1].text.strip()
            languages[lang_code] = lang_name
            
    if languages:
        for code, name in languages.items():
            langs.append(name)
            
    return langs