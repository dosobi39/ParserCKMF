import os
import re
import csv
import sys
import time
import shutil
import requests
# import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

version = 1.1

print(f"--------------------------------------------------------\n"
      f"     ----------  Parser_ckmf_ru__V-{version}  ------------     \n"
      f"--------------------------------------------------------\n")

time.sleep(1)

product_name = None
product_availability = None
product_article = None
product_price = None
product_url = None
urls = None
s_urls = None


def get_all_pages():
    global s_urls, urls
    # Нужна проверка правильности ссылок
    # urls = "https://ckmf.ru/catalog/komplektuyushchie_dlya_myagkoy_mebeli/napolniteli_dlya_mebeli/porolon/"
    urls = input("Введите ссылку на каталог товаров >> ")
    s_urls = re.search("(?P<url>https?://[^\s]+)", urls).group()

    # print("[!!INFO!!] Введите корректную ссылку")

    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
    }

    r = requests.get(urls, headers=headers)

    # Создание директории для html файлов
    if not os.path.exists("data_html"):
        os.mkdir("data_html")
        # print("[*INFO*] Создана директория 'data_html'")

    with open("data_html/page_1.html", "w", encoding="iso_8859_1") as file:
        file.write(r.text)

    with open("data_html/page_1.html", encoding="iso_8859_1") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    try:
        pages_count = int(soup.find("div", class_="nums").find_all("a")[-1].text)
    except AttributeError:
        pages_count = 1

    for i in range(1, pages_count + 1):
        url = f"{urls}?PAGEN_1={i}"
        print(f"Получение кода страницы {i}")

        r = requests.get(url=url, headers=headers)
        with open(f"data_html/page_{i}.html", "w", encoding="iso_8859_1") as file:
            file.write(r.text)

        time.sleep(2)

    return pages_count + 1


def collect_data(pages_count):
    global product_name, product_availability, product_price, product_article, product_url
    # Создание директории для готовых файлов
    if not os.path.exists("out_data"):
        os.mkdir("out_data")
        print("[*INFO*] Создана директория 'out_data'")

    cur_date = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    # cur_date = datetime.now().strftime("%d_%m_%Y")

    with open(f"out_data/data_{cur_date}.csv", "w", newline="", encoding="utf-8") as file:    # , encoding="cp1251"
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

        with open(f"data_html/page_{page}.html", encoding="utf-8") as file:   # , encoding="utf-8"
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        items_cards = soup.find_all("div", class_="item_info")

        no_value = "------"
        for item in items_cards:

            # Название
            try:
                product_name = item.find("a", class_="dark_link option-font-bold font_sm").text.replace('\xd7', 'x')
                print('Наименование - ', product_name)

            except AttributeError:
                print("[INFO] Название отсутствует, строка заполнена", no_value)

            # Наличие
            try:
                product_availability = item.find("span", class_="value font_sxs").text.strip()
                print('Наличие ------ ', product_availability)

            except AttributeError:
                print("[INFO] Аттрибут 'Наличие' отсутствует, строка заполнена", no_value)

            # Артикул
            try:
                product_article = item.find("div", class_="muted font_sxs").text.lstrip("Арт.: ")
                print('Артикул ------ ', product_article)

            except AttributeError:
                print("[INFO] Артикул отсутствует, строка заполнена", no_value)

            # Цена
            try:
                product_price = item.find("span", class_="price_value").text.strip('nbsp')
                print('Цена --------- ', product_price)

            except AttributeError:
                print("[INFO] Цена отсутствует, строка заполнена", no_value)

            # Ссылка на товар
            product_url = f'https://ckmf.ru{item.find("a", href=True)["href"]}'
            print('Ссылка ------- ', product_url)

            product_count += 1
            print("[INFO] Получено товаров -", product_count, "\n")

            data.append(
                {
                    "product_article": product_article,
                    "product_name": product_name,
                    "product_url": product_url,
                    "product_availability": product_availability,
                    "product_price": product_price
                }
            )

            with open(f"out_data/data_{cur_date}.csv", "a", newline="", encoding="utf-8") as file:    # , encoding="cp1251"
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
    os.system("cls")

    print(f"-------------------------------------------------------\n"
          f"[INFO] Парсинг товаров по ссылке выполнен\n"
          f"[INFO] Обработано страниц - {page}\n"
          f"[INFO] Получено товаров -", product_count, "\n"
          f"-------------------------------------------------------\n"
          f"[INFO] Товары сохранены в директорию 'output_data'\n"
          f"-------в файл 'data_{cur_date}.csv'\n"
          f"-------------------------------------------------------\n"
          f"--Для завершения работы введите 'exit'\n"
          f"--или закройте программу\n"
          f"-------------------------------------------------------\n")

    # Перекодировоние файла в UTF-8
    # path = f"out_data/data_{cur_date}.csv"
    # df = pd.read_csv(path, encoding='latin1', errors="replace")    # cp1251
    # df.to_csv(path, encoding='utf-8', index=False, errors="replace")

    # Заготовка для получения файла json
    # with open(f"out_data/data_{cur_date}.json", "a") as file:
    #     json.dump(data, file, indent=4, ensure_ascii=False)


# Удаление директории "data" вместе со всеми файлами
def remove_dir_data_html():
    if os.path.exists("data_html"):
        shutil.rmtree("data_html")
        # print("[*INFO*] Директория 'data_html' и вложенные 'html' файлы удалены")


def main():
    global s_urls, urls
    while True:

        url_ok = False
        while not url_ok:
            try:
                pages_count = get_all_pages()
                collect_data(pages_count=pages_count)
                remove_dir_data_html()
                time.sleep(1)
            except AttributeError:
                if urls == 'exit':
                    sys.exit()
                os.system("cls")
                print("-----------------------------------------------\n"
                      "[INFO] Вы ввели некорректную ссылку\n"
                      "------ повторите попытку\n"
                      "-----------------------------------------------\n"
                      "-- Для завершения работы введите 'exit'\n"
                      "-- или закройте программу\n"
                      "-----------------------------------------------\n")

                time.sleep(1)
            else:
                url_ok = True


if __name__ == '__main__':
    main()
