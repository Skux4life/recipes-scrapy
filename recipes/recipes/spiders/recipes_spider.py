import scrapy

class RecipesSpider(scrapy.Spider):
    # def create_start_urls():
    #     base_url = 'https://www.recipetineats.com/recipes/?fwp_paged='
    #     start_urls = []
    #     for i in range(1, 62): #need to use start_requests I think
    #         start_urls.append(f'{base_url}{i}')
    #     return start_urls

    name = 'recipes'
    start_urls =  ['https://www.recipetineats.com/recipes']           #create_start_urls()

    def parse(self, response):
        for recipe in response.xpath('//main//article'):
            yield {
                'title': recipe.xpath('.//h2/a[@class="entry-title-link"]/text()').get(),
                'link': recipe.xpath('.//h2/a[@class="entry-title-link"]/@href').get(),
            }

        next_page = response.xpath('.//div[@class="facetwp-pager"]//li[@class="pagination-next"]/a/@data-page').get()
        if next_page is not None:
            yield response.follow(f'https://www.recipetineats.com/recipes/?fwp_paged={next_page}', callback=self.parse)

    
        
