import csv
import pandas as pd
import os
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from termcolor import colored
import shutil

print(colored("--------------------------------------------------------\n"
      "*** Парсер работает только с сайтом ckmf.ru ***\n"
      "--------------------------------------------------------\n"
      "* Все отсутствующие данные записываются как '------' *\n"
      "--------------------------------------------------------\n", 'red'))

urls = input("Введите ссылку на каталог товаров >> ")


def get_all_pages():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
    }

    r = requests.get(urls, headers=headers)

    # Создание директории для html файлов
    if not os.path.exists("data_html"):
        os.mkdir("data_html")
        print(colored("[*INFO*] ", 'red') + "Создана директория 'data_html'")

    with open("data_html/page_1.html", "w", encoding="iso_8859_1", errors="ignore") as file:
        file.write(r.text)

    with open("data_html/page_1.html", encoding="iso_8859_1", errors="ignore") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    try:
        pages_count = int(soup.find("div", class_="nums").find_all("a")[-1].text)
    except AttributeError:
        pages_count = 1

    for i in range(1, pages_count + 1):
        url = f"{urls}?PAGEN_1={i}"
        print(url)

        r = requests.get(url=url, headers=headers)
        with open(f"data_html/page_{i}.html", "w", encoding="iso_8859_1", errors="ignore") as file:
            file.write(r.text)

        time.sleep(2)

    return pages_count + 1


def collect_data(pages_count):

    # Создание директории для готовых файлов
    if not os.path.exists("out_data"):
        os.mkdir("out_data")
        print(colored("[*INFO*] ", 'red') + "Создана директория 'out_data'")

    cur_date = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")

    with open(f"out_data/data_{cur_date}.csv", "w", encoding="cp1251") as file:  # encoding="utf-8"
        writer = csv.writer(file)

        writer.writerow(
            (
                "Артикул",
                "Название",
                "Ссылка на товар",
                "Наличие",
                "Цена"
            )
        )
    data = []

    product_count = 0
    for page in range(1, pages_count):

        with open(f"data_html/page_{page}.html", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        items_cards = soup.find_all("div", class_="item_info")

        for item in items_cards:

            # Название
            try:
                product_name = item.find("a", class_="dark_link option-font-bold font_sm").text.strip()
                print(product_name)
            except AttributeError:
                print(colored("[*INFO*] ", 'red') + "Название отсутствует, строка заполнена '------'")

            # Наличие
            try:
                product_availability = item.find("span", class_="value font_sxs").text.strip()
                print('product_availability-', product_availability)
            except AttributeError:
                print(colored("[*INFO*] ", 'red') + "Аттрибут 'Наличие' отсутствует, строка заполнена  '------'")

            # Артикул
            try:
                product_article = item.find("div", class_="muted font_sxs").text.lstrip("Арт.: ")
                print('product_article-', product_article)
            except AttributeError:
                print(colored("[*INFO*] ", 'red') + "Артикул отсутствует, строка заполнена  '------'")

            # Цена
            try:
                product_price = item.find("span", class_="price_value").text.strip()
                print('product_price-', product_price)
            except AttributeError:
                print(colored("[*INFO*] ", 'red') + "Цена отсутствует, строка заполнена  '------'")

            # Ссылка на товар
            product_url = f'https://ckmf.ru{item.find("a", href=True)["href"]}'
            print(colored("[*INFO*] ", 'red') + "Ссылка на товар -", product_url)

            product_count += 1
            print(colored("[*INFO*] ", 'red') + "Получено товаров -", product_count, "\n")

            data.append(
                {
                    "product_article": product_article,
                    "product_name": product_name,
                    "product_url": product_url,
                    "product_availability": product_availability,
                    "product_price": product_price
                }
            )

            with open(f"out_data/data_{cur_date}.csv", "a", encoding="cp1251") as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        product_article,
                        product_name,
                        product_url,
                        product_availability,
                        product_price
                    )
                )
        page_info = f"{page}"
        print(colored("[*INFO*] ", 'red') + "Обработано страниц ", page_info)

    # Перекодировоние файла в UTF-8
    path = f"out_data/data_{cur_date}.csv"
    df = pd.read_csv(path, encoding='cp1251')
    df.to_csv(path, encoding='utf-8', index=False)

    # Заготовка для получения файла json
    # with open(f"out_data/data_{cur_date}.json", "a") as file:
    #     json.dump(data, file, indent=4, ensure_ascii=False)


# Удаление директории "data" вместе со всеми файлами
def remove_dir_data_html():
    if os.path.exists("data_html"):
        time.sleep(5)
        shutil.rmtree("data_html")
        print(colored("[*INFO*] ", 'red') + "Директория 'data_html' и вложенные 'html' файлы удалены")


def main():
    pages_count = get_all_pages()
    collect_data(pages_count=pages_count)
    remove_dir_data_html()


if __name__ == '__main__':
    main()
