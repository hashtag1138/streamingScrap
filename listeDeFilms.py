import requests
from lxml import etree
import sys, os
import concurrent.futures
import filmPage
from manageFile import writeJson, existJson
from selenium import webdriver

def fetch(url):
    r = requests.get(url)
    if r.status_code != 200:
        return False
    else:
        html = r.text
        return html
def getAffiches(url):
    html = fetch(url)
    tree = etree.HTML(html)
    return [parseDiv(div) for div in tree.xpath("//div[@class='affiche']")]
def parseDiv(div):
    return {'title' : getTitle(div), 'img': getImg(div), 'href': getHref(div)}
def getTitle(div):
    return "".join(div.xpath("./a[1]/@title"))
def getImg(div):
    return {'src' : "".join(div.xpath("./a[1]/img/@src")), "height" : int("".join(div.xpath("./a[1]/img/@height"))),
            'width' : int("".join(div.xpath("./a[1]/img/@width")))}
def getHref(div):
    return "".join(div.xpath("./a[1]/@href"))

def scrapPage(url):
    try :
        chrome = filmPage.newBrowser()
        affichesList = [affiche for affiche in getAffiches(url) if not existJson(affiche['title'])]
        filmsDic = [writeJson(extend(filmPage.getFilmDetail(chrome, affiche['href']), affiche['img'])) for affiche in affichesList]
        print("[SCRAPED {} films at {}]".format(str(len(filmsDic)), url))
    except Exception as e:
        print(e)
        pass
    if isinstance(chrome, webdriver.chrome.webdriver.WebDriver):
        chrome.quit()

def extend(filmDic, imgDic):
    filmDic['img'] = imgDic
    return filmDic

def scrapRange( startIndex, stopIndex, maxthread=2):
    urls = ["".join(["http://www.filmcomplet.tv/films-en-streaming-page-",str(number),'.html']) for number in range(startIndex,stopIndex)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=maxthread) as executor:
        executor.map(scrapPage, urls)
if __name__ == "__main__":
    scrapRange(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
  

