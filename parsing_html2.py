from bs4 import BeautifulSoup
import json

# Вторая
# Из html получаем данные в Json

# Открываю файл на чтение
with open('index.html', "r", encoding="utf-8") as file:
    scr = file.read()

soup = BeautifulSoup(scr, 'lxml')

all_products_hrefs = soup.find_all(class_="mzr-tc-group-item-href") # Ищем все ссылки


all_categories_dict = {}
for i in all_products_hrefs:    # цикл для выводы продуктов и ссылок
    i_text = i.text
    i_href = "https://health-diet.ru" + i.get("href")
    # print(f"{i_text}: {i_href}") # Показываю название продукта и ссылку на неё
    # print(f"{i_text}: {i_href}") # вывожу уже действюущую ссылку (гиперссылку)
    all_categories_dict[i_text] = i_href # наполняем словарик именами и ссылки

with open ("all_categories_dict.json", "w", encoding='utf-8') as file:
    json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)