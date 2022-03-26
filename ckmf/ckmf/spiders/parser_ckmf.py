import csv

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.item import Item, Field


class ParserCkmfSpider(CrawlSpider):
    name = 'parser_ckmf'
    allowed_domains = ['ckmf.ru']

    # список категорий
    start_urls = ['https://ckmf.ru/catalog/',
                  ]

    # allow =(разрешающие фильтры для парсинга)
    # deny=(запрещающие фильтры для парсинга)

    rules = (Rule(LinkExtractor(allow=('/izdeliya_iz_drevesiny/',
                                       '/komplektuyushchie_dlya_korpusnoy_mebeli/',
                                       '/mebelnye_tkani/',
                                       '/kleevye_materialy/',
                                       '/kovriki_setki/',
                                       '/komplektuyushchie_dlya_myagkoy_mebeli/',
                                       '/matrasnye_tkani/',
                                       '/napolniteli_dlya_matrasov/',
                                       ),
                                deny=('/rasrodazha/', '/brands/', '/company/', '/help/', '/personal/', '/basket/', '/sale/',
                                      '/contacts/', '/info/', '/filter', '/?display=', '/?sort=', '/?linerow*',
                                      'https://ckmf.ru:443/',)),
                  callback='parse', follow=True),)

    # создаем CSV с названиями столбцов
    with open('D:/Python_Project/ParserCKMF/CKMF_parse.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                'Артикул',
                'Название',
                'Ссылка на товар',
                'Наличие',
                'Цена',
                'Описание',
            )
        )

    def parse(self, response):
        data = []

        # название
        title = response.xpath('//div[@class="topic__heading"]//h1[1]/text()').get()

        # артикул
        article = response.xpath('//span[@itemprop="value"]/text()').get()

        # ссылка на товар
        product_link = response.url

        # наличие
        availability = response.xpath('(//div[@class="item-stock "])[2]//span[@class="value font_sxs"]/text()').get()

        # цена
        price = response.xpath('(//div[@class="prices-wrapper"])[1]//span[@class="price_value"]/text()').get()

        # описание
        descriptions = response.xpath('(//div[@class="ordered-block desc"]//div)[2]/text()').get()

        # если по ссылке найден Артикул, то все собранные данные со страницы добавляем в список data
        if article is not None:
            data.append(
                {
                    'article': article,
                    'title': title,
                    'product_link': product_link,
                    'availability': availability,
                    'price': price,
                    'descriptions': descriptions,
                }
            )

            # замисываем данные из data в CSV
            with open('D:/Python_Project/ParserCKMF/CKMF_parse.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        article,
                        title,
                        product_link,
                        availability,
                        price,
                        descriptions,
                    )
                )
