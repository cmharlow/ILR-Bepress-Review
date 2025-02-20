import requests
from lxml import html
import json

URLS = []
webdata = {}
with open('data/urls.txt') as fh:
    URLS = fh.read().splitlines()
with open('data/webscrape/data.json') as fh:
    webdata = json.load(fh)

for url in URLS[24388:]:
    print('scraping ' + url)
    webdata[url] = {}
    resp = requests.get(url)
    tree = html.fromstring(resp.content)
    metatags = {}
    for meta in tree.xpath('//meta'):
        name = meta.get('name')
        if name is not 'viewport':
            metatags[meta.get('name')] = meta.get('content')
    webdata[url]['meta'] = metatags
    series_title = series_url = None
    sertitle_xp = "//div[@id='series-header']/h2[@id='series-title']/a"
    series_titles = tree.xpath(sertitle_xp)
    for title in series_titles:
        series_title = title.text
    serurl_xp = "//div[@id='series-header']/h2[@id='series-title']/a"
    series_urls = tree.xpath(serurl_xp)
    for ser_url in series_urls:
        series_url = ser_url.get('href')
    webdata[url]['series_title'] = series_title
    webdata[url]['series_url'] = series_url
    for elem in tree.xpath('//div[@id="alpha"]/*'):
        if elem.get('id') == 'title':
            for val in elem.xpath('p/a'):
                webdata[url]['fulltext_url'] = val.get('href')
                webdata[url][elem.get('id')] = val.text
        else:
            for val in elem.xpath('p'):
                webdata[url][elem.get('id')] = val.text
    with open('data/webscrape/data.json', 'w') as fh:
        json.dump(webdata, fh)


def grabURLs():
    URLS = []
    with open('data/urls.txt') as fh:
        URLS = fh.read().splitlines()
    return(URLS)


def getMetatags(html):
    """Get Meta tags values from HTML passed, return values as dict."""
    metatags = {}
    for meta in html.xpath('//meta'):
        name = meta.get('name')
        if name is not 'viewport':
            metatags[meta.get('name')] = meta.get('content')
    return(metatags)


def getSeries(html):
    series_title = series_url = None
    sertitle_xp = "//div[@id='series-header']/h2[@id='series-title']/a"
    series_titles = html.xpath(sertitle_xp)
    for title in series_titles:
        series_title = title.text
    serurl_xp = "//div[@id='series-header']/h2[@id='series-title']/a"
    series_urls = html.xpath(serurl_xp)
    for url in series_urls:
        series_url = url.get('href')
    return(series_title, series_url)


def getAlphaDiv(html, output, url):
    for elem in html.xpath('//div[@id="alpha"]/*'):
        if elem.get('id') == 'title':
            for val in elem.xpath('p/a'):
                output[url]['fulltext_url'] = val.get('href')
                output[url][elem.get('id')] = val.text
        else:
            for val in elem.xpath('p'):
                output[url][elem.get('id')] = val.text
    return(output)


def scrapeURLs(URLS):
    webdata = {}
    output = {}
    for url in URLS:
        print('scraping ' + url)
        webdata[url] = {}
        resp = requests.get(url)
        tree = html.fromstring(resp.content)
        webdata[url]['meta'] = getMetatags(tree)
        (series_title, series_url) = getSeries(tree)
        webdata[url]['series_title'] = series_title
        webdata[url]['series_url'] = series_url
        output = getAlphaDiv(tree, webdata, url)
    return(output)


def main():
    URLS = grabURLs()
    resp = scrapeURLs(URLS)
    with open('data/webscrape/data.json', 'wb') as fh:
        json.dump(resp, fh)


if __name__ == '__main__':
    main()
