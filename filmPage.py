from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time
import sys

def newBrowser(wait=2):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    browser = webdriver.Chrome(chrome_options=options)
    return browser

def getStreamSrc(browser,players):
    iframesrc = []
    for elm in players:
        try: 
            browser.find_element_by_xpath("//*[@id='lecteurs']/div[@class='bloc-hebergeur']/div/div/div[@heberger='" +elm+ "']/button").click()
            time.sleep(0.5)
            iframesrc.append(browser.find_element_by_xpath("//*[@id='lecteurs']/div['well bande_item col-md-12']/div/iframe").get_attribute('src'))
            browser.refresh()
        except:
            pass
    return iframesrc
def getTitle(browser):
    return browser.find_element_by_xpath("//*[@id='content']/div[1]/h1").text
def getDescription(browser):
    txt = browser.find_element_by_xpath("//*[@id='content']/div[@class='xoopstube_descriptions']").text
    txt = txt.split('\n')
    if len(txt) == 5:
        return {'durée' : getDuree(txt[0]), 'acteurs': getActeurs(txt[1]), 'realisateur' : getReal(txt[2]),
            'genre' : getGenre(txt[3]), 'synopsis': getSynopsis(txt[4])}
    else:
        return {'Durée' : getDuree(txt[0]), 'Acteurs': getActeurs(txt[1]), 'Synopsis': txt[2]}
def getDuree(txt):
    if txt.find('Durée:') > -1:
        return toSeconds(txt.split(':', 1)[1]) # 1h30 -> 5400
def toSeconds(txt):
    if txt.find('h')>-1 and txt.find('min')>-1 :
        heure = int(txt.split('h')[0])
        minute = int(txt.split('h')[1][:-len('min')])
        return heure*3600+minute*60
    else:
        splited = txt.split(':')
        return int(splited[0])*3600+ int(splited[1])*60 + int(splited[2])
def getActeurs(txt):
    if txt.find('Avec') > -1:
        return txt.split(':')[1].split(',')
def getReal(txt): 
    if txt.find('Réalisé par') > -1:
        return txt.split(':')[1]
def getGenre(txt):
    if txt.find('Genre') > -1:   
        return txt.split(':')[1].split(',')
def getSynopsis(txt):    
    if txt.find('Synopsis:') > -1:
        return txt.split(':')[1]

def getFilmDetail(chrome, url):
    chrome.get(url)
    fulllist = [ 'uqload', 'openload', 'streamango', 'mystream', 'uptostream', 'netu','youwatch']
    description = {'title': getTitle(chrome),
            'description' : getDescription(chrome), 'streams': getStreamSrc(chrome, fulllist)}
    return description

if __name__ == "__main__":
    print(getFilmDetail(sys.argv[1]))

