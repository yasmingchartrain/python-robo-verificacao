import scrapy
import re


def valid(url):
    if url is None:
        print(url, " NULO")
        return False

    if url.startswith('tel'):
        print(url, "TEL")
        return False
    return True

def sanitize(url):
   regex = r"((?:?|&)redirect=[^(?:&|\s]*)"
   return re.sub(regex, "", url)



class SescSpider(scrapy.Spider):
    name = 'sesc'
    allowed_domains = ['sesc.seatecnologia.com.br']
    start_urls = ['https://sesc.seatecnologia.com.br/']


    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 ' \
                 'Safari/537.36'

    def parse(self, response):
        url_erro = []
        links = response.css('a::attr(href)').getall()
        for url in links:
            if 'sescdf.com.br' in url:
                url_erro.append(url)

        yield {
            'url': response.url,
            'url_erro': response.url_erro.join()
        }
        for url in links:
            if valid(url):
                full_url = response.urljoin(url)
                full_url = sanitize(full_url)
                yield scrapy.Request(full_url)

