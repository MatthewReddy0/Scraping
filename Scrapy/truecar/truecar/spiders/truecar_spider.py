import scrapy

"""
pipenv shell
(scrapy) scrapy startproject truecar
(scrapy) scrapy crawl truecar -o truecar.csv

scrapy shell 'https://en.wikipedia.org/wiki/Tesla,_Inc.'
>>> response.css
('table.wikitable tbody').get()
>>> view(response)

scrapy shell -s USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36' 'https://www.truecar.com/used-cars-for-sale/listings/tesla/model-3/'

Create truecar_spider.py in truecar/spiders

To quit the shell, Ctrl+D
"""


# Spider for truecar.com
class TruecarSpider(scrapy.Spider):

    name = "truecar"

    def start_requests(self):

        urls = ['https://www.truecar.com/used-cars-for-sale/listings/tesla/model-3/']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        # Uses xpath (from Developer Tools) to generate a list of all the listing
        # Data might not be in divs, you'll have to look this up
        all_listings = response.xpath('//div[@data-qa="Listings"]')

        for tesla in all_listings:

            make_model = tesla.css('div[data-test="vehicleListingCardTitle"] > div')
            year = make_model.css('span.vehicle-card-year::text').get()
            model_raw = make_model.css('span.vehicle-header-make-model').get()
            model = model_raw[model_raw.find('>')+1:-7].replace('<!-- -->', '')

            # These are a bunch of selectors
            # The column headings from the csv file
            tesla_data = {
                'url': 'http://truecar.com' + tesla.css('a::attr(href)').get(),
                'model': year + ' ' + model,
                'mileage': tesla.css('div[data-test="cardContent"] > div > div.text-truncate::text').get(),
                'price': tesla.css('h4::text').get()
            }

            yield tesla_data
