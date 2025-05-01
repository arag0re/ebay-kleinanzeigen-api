from lxml import etree
from nodriver import Browser, Tab, Element, cdp, start
from bs4 import BeautifulSoup
import requests
import time

from functions.getProxy import *
from functions.getUserAgent import *

async def getInseratDetails(url):
    try:
        start_time = time.time()

        proxy = getProxy()

        browser = await start(
            browser_args=[
                "--headless=new",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-web-security",
                "--disable-site-isolation-trials",
                "--incognito",
                "--user-agent=" + GET_UA(),
            ]
        )
        

        tab = await browser.get(url)

        try:
            title = driver.find_element(By.XPATH, '//*[@id="viewad-title"]').text
            for s1 in title:
                title = title.strip()
        except:
            title = "NotFound"

        try:
            price = driver.find_element(By.XPATH, '//*[@id="viewad-main-info"]/meta[1]').get_attribute('content')
        except:
            price = "0"

        try:
            views = driver.find_element(By.XPATH, '//*[@id="viewad-cntr-num"]').text
        except:
            views = 0

        def extract_source(url):
            agent = {'User-Agent': GET_UA()}
            proxyOption = {'http': proxy}
            source=requests.get(url, headers=agent, proxies=proxyOption)
            return source

        def getImages(url):
            page = extract_source(url)
            soup = BeautifulSoup(page.content, "html.parser")
            dom = etree.HTML(str(soup))
            imgSrcDivs = soup.find_all('div',{"class":"galleryimage-element"})
            imgSrcArr = []
            for imgSrcDiv in imgSrcDivs:
                if imgSrcDiv:
                    imgSrc = imgSrcDiv.find('img')
                    if imgSrc:
                        src = imgSrc['src']
                        imgSrcArr.append(src)

            return(imgSrcArr)

        imgSrcArr1 = getImages(url)

        tagsSrcDivs = driver.find_elements(By.CLASS_NAME, 'breadcrump-link')
        tagsSrcArr = []
        for tagSrcDiv in tagsSrcDivs:
            getTags = tagSrcDiv.find_element(By.TAG_NAME, 'span').text
            tagsSrcArr.append(getTags)

        try:
            description = driver.find_element(By.XPATH, '//*[@id="viewad-description-text"]').text
            for s2 in description:
                description = description.strip()
        except:
            description = "NotFound"

        try:
            uploadDate = driver.find_element(By.XPATH, '//*[@id="viewad-extra-info"]/div[1]/span').text
        except:
            uploadDate = "0000-00-00"

        try:
            adId = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/section[1]/section/aside/div[3]/ul/li[2]').text
        except:
            adId = "0"

        data = {'title':title, 'price': price, 'images':imgSrcArr1, 'tags':tagsSrcArr, 'views':views, 'description':description, 'uploadDate':uploadDate, 'adId':adId}

        end_time = time.time()

        print("getInseratDetails.py execution:")
        print(str(round(end_time - start_time, 2))+" seconds")
        print("Proxy: "+proxy)
        driver.quit()
        return (data)
    except Exception as e:
        print(e)
        driver.quit()
        return None
