import random
from time import sleep
from bs4 import BeautifulSoup
import json
import requests
from fake_useragent import UserAgent
import csv

# Третий
# Получаем данные из jsnon и из разделов категорий

ua = UserAgent()
headers = ua.random

# читаем json и вносим всё в переменную
with open("all_categories_dict.json", encoding='utf-8') as file:
    all_categories = json.load(file)

# Информация о старте
iteration_count = int(len(all_categories)) - 1
count = 0
print(f"Всего итерации: {iteration_count}")

for categories_name, categories_href in all_categories.items():

    # Меняем знаки на _
    rep = [",", " ", "-", "'"]
    for item in rep:
        if item in categories_name:
            categories_name = categories_name.replace(item, "_")

    # Снова делаем запрос, но уже в категории
    req = requests.get(url=categories_href, headers={"User-agent": headers})
    scr = req.text
    # Сохраняем страницу HTML под именем категории
    with open(f'data/{count}_{"categories_name"}.html', "w", encoding="utf-8") as file:
        file.write(scr)

    # Открываем и сохраняем код страницы
    with open(f'data/{count}_{"categories_name"}.html', "r", encoding="utf-8") as file:
        scr = file.read()

    soup = BeautifulSoup(scr, "lxml")

    # Проверка страницы на наличие таблицы с продуктами
    alert_block = soup.find(class_="uk-alert-danger")
    if alert_block is not None:
        continue

    # Собираем Заголовки таблицы
    table_head = soup.find(class_="mzr-tc-group-table").find("tr").find_all("th")
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fails = table_head[3].text
    carbohydrates = table_head[4].text

    # Открываем файл на запись для Заголовков
    with open(f"data/{count} - {categories_name}.scv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fails,
                carbohydrates
            )
        )

    # Собираем данные продуктов
    products_data = soup.find(class_="mzr-tc-group-table").find("tbody").find_all("tr")

    # Переменная для json
    products_info = []

    # Проходимся циклом, чтобы собрать все продукты
    for item in products_data:
        products_tds = item.find_all("td")

        title = products_tds[0].find("a").text
        calories = products_tds[1].text
        proteins = products_tds[2].text
        fats = products_tds[3].text
        carbohydrates = products_tds[4].text

        # Добавляем в переменную для создания в json
        products_info.append(
            {
                "Title": title,
                "Calories": calories,
                "Proteins": proteins,
                "Fats": fats,
                "Carbohydrates": carbohydrates
            }
        )

        # Дозапись в scv
        with open(f"data/{count} - {categories_name}.scv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fails,
                    carbohydrates
                )
            )

            # Запись в scv в json
            with open(f"data/{count}_{categories_name}.json", "a", encoding="utf-8") as file:
                json.dump(products_info, file, indent=4, ensure_ascii=False)

    count += 1
    print(f"Итерация {count}. {categories_name}  - записан!")
    iteration_count -= 1

    if iteration_count == 0:
        print("Done!")

    print(f"Осталось {iteration_count} итераций")

    # sleep(random.randrange(2, 4)) #Просто чтобы было
