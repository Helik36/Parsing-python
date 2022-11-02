import requests
from fake_useragent import UserAgent

# Данный код разбил на несколько частей чтобы видно весь код и всю работу
# Первый.
# Сначала выполняем это часть кода чтобы получить страницу html от куда будем получать данные

url = 'https://health-diet.ru/table_calorie/'

# создаю юзер агента
ua = UserAgent()
headers = ua.random

req = requests.get(url, headers={"User-agent": headers}) # отправляю get Запрос с юзерагентом что мы не бот
scr = req.text # получаю текст html
# print(req) # получаю ответ код
# print(scr) # получаю текст страницы

with open('index.html', "w", encoding="utf-8") as file: # чтобы постоянно не парсить сайт, сохраняю файл себе
    file.write(scr)
