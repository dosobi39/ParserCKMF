import csv

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.item import Item, Field


class ParserCkmfSpider(CrawlSpider):
    name = 'parser_ckmf'
    allowed_domains = ['ckmf.ru']
    start_urls = ['https://ckmf.ru/catalog/izdeliya_iz_drevesiny/',
                  'https://ckmf.ru/catalog/komplektuyushchie_dlya_korpusnoy_mebeli/',
                  'https://ckmf.ru/catalog/mebelnye_tkani/',
                  'https://ckmf.ru/catalog/kleevye_materialy/',
                  'https://ckmf.ru/catalog/kovriki_setki/',
                  'https://ckmf.ru/catalog/komplektuyushchie_dlya_myagkoy_mebeli/',
                  'https://ckmf.ru/catalog/matrasnye_tkani/',
                  'https://ckmf.ru/catalog/napolniteli_dlya_matrasov/',
                  ]

    rules = (Rule(LinkExtractor(allow=('/fanera_dsp_dvp/', '/lameli_i_latoderzhateli/',
                                       '/nakladki/', '/shkant_shtanga/', '/karton_fanera_dsp_dvp/',
                                       '/napravlyayushchie_2/', '/opory_mikron/', '/petli_kronshteyny/', '/ugolki_profil/',
                                       '/ruchki/', '/truby_derzhateli_zaglushki/', '/furnitura_raznoe/', '/moyki/',
                                       '/napolnenie_shkafov/', '/smesiteli/', '/iskusstvennaya_kozha/', '/tkani/',
                                       '/umnye_tkani_smart/', '/tkani_s_printom/', '/kleevye_sterzhni_kley_dlya_kromki/',
                                       '/kley_dlya_porolona/', '/kley_drevesnyy/', '/oborudovanie_dlya_kleya/',
                                       '/razbavitel_dlya_kleya/', '/kovriki_setki/', '/mekhanizmy_i_prochie_komplektuyushchie/',
                                       '/netkanye_materialy/', '/napolniteli_dlya_mebeli/', '/opory_mebelnye/', '/skoba_instrument/',
                                       '/metizy/', '/raznoe/', '/tkanye_materialy/', '/shveynaya_furnitura/', '/aksessuary_1/',
                                       '/dekorativnye_gvozdi_lenty/', '/kanty_kordy_profili/', '/matrasnye_tkani/',
                                       '/bonel_dlya_matrasov/', '/volnit_laytek/', '/kokosovaya_koyra/', '/lateks/',
                                       '/furnitura_dlya_matrasov/',
                                       ),
                                deny=('/rasrodazha/', '/brands/', '/company/', '/help/', '/personal/', '/basket/', '/sale/',
                                      '/contacts/', '/info/', '/filter', '/?display=', '/?sort=', '/?linerow*',)),
                  callback='parse', follow=True),)

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
        product_link = product_url = response.url

        # наличие
        availability = response.xpath('(//span[@class="value font_sxs"])[3]/text()').get()

        # цена
        price = response.xpath('(//div[@class="prices-wrapper"])[1]//span[@class="price_value"]/text()').get()

        # описание
        descriptions = response.xpath('(//div[@class="ordered-block desc"]//div)[2]/text()').get()

        # # описание
        # descriptions = str(response.xpath('((//div[@class="item-info__desc"])[1]//p)/text()').get())
        #
        # # название характеристики
        # specifications_1 = response.xpath('(//div[@class="item-info__specs"]/ul)[1]/li/p[1]/text()').getall()
        # specifications_1 = [x.strip() for x in specifications_1]
        # # specification_1 = ['\n'.join(specifications_1)]
        #
        # # значение характеристики
        # specifications_2 = response.xpath('(//div[@class="item-info__specs"]/ul)[1]/li/p[2]/text()').getall()
        # specifications_2 = [x.strip() for x in specifications_2]
        #
        # # обЪединение названия и значения характеристик "Название: значение"
        # specification = [': '.join(x) for x in zip(specifications_1, specifications_2)]
        # specification = ', '.join(specification)
        #
        # # преимущества
        # advantages = response.xpath('(//div[@class="item-info__lists"])[1]/ul/li/text()').getall()
        # advantages = [x.strip() for x in advantages]
        # advantage = ', '.join(advantages)
        #
        # # старая цена
        # old_price = response.xpath('//p[@class="item-header__price product__price--old"]//span[1]/text()[2]').get()
        #
        # # новая цена
        # new_price = response.xpath('//p[@class="item-header__price"]//span[1]/text()[2]').get()
        #
        # # размер скидки
        # discount = response.xpath(
        #     '(//div[@class="item-header__prices"]//p[@class="item-header__price product__price--sale"]//span)/text()').get()
        #
        # # собираем ссылки картинок товара
        # img_url = response.xpath('(//div[@class="swiper-wrapper"])[1]//div[@class="item-slider__img"]/a/@href').getall()
        # img_url = ['https://mnogomebeli.com' + x for x in img_url]
        # img_urls = ', '.join(img_url)
        #
        # # собираем ссылки фотографий чертежей
        # drawing = response.xpath('//div[@class="item-info__col"]//img/@src').getall()
        # drawing = ['https://mnogomebeli.com' + draw.split('?')[0] for draw in drawing]
        #
        # # собираем ссылки на доп фото
        # other_photo = response.xpath('(//div[@class="swiper-wrapper"])[3]//img[@class="img__i"]/@src').getall()
        # other_photo = ['https://mnogomebeli.com' + o_p.split('?')[0] for o_p in other_photo]
        #
        # # проверяем список на одинаковые ссылки
        # for url_o_p in drawing:
        #     if url_o_p not in other_photo:
        #         # объединаяем ссылки чертежей и доп. фото в один список
        #         other_photo.append(url_o_p)
        #
        # other_photo = list(dict.fromkeys(other_photo))
        # other_photos = ', '.join(other_photo)

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
