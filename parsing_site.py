import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

url = 'https://health-diet.ru/table_calorie/'

# создаю юзер агента
ua = UserAgent()
headers = ua.random

req = requests.get(url, headers={"User-agent": headers}) #отправляю get Запрос с юзерагентом что мы не бот
scr = req.text # получаю текст html
print(req) # получаю ответ код
print(scr) # получаю текст страницыв

with open('index.html', "w") as file: # чтобы постоянно не парсить сайт и не получить бан, сохраняем html страницу
    file.write(scr)
