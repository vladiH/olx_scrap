
# coding: utf-8

# In[ ]:


import keyboard  
import random
import requests
import uuid
import io
import multiprocessing as mp
import logging
from PIL import Image
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
# In[ ]:


log = logging.getLogger(__name__)


# In[ ]:


class SeleniumScrapy():
    #pDbConnexion(sqlalchemy connexion)
    #pTypeBrowser(String): f:firefox, c:chrome
    #pBrowserDrive(String): path for browser drive 
    #pOlxUrlAutos(String):http link from autos https://www.olx.com.pe/"AUTOS_PERU"
    #pOutDir(String):output path for results
    #pDownloadImage(bool):true, download image from olx else omit it
    def __init__(self, pTypeBrowser, pBrowserDrive, pOlxUrlAutos, pOutDir, pDownloadImage=False ):
        self._TypeBrowser=pTypeBrowser
        self._browserDrive = pBrowserDrive
        self._olxUrlAutos = pOlxUrlAutos
        self._outDir = pOutDir
        
        self._thresholdPrice=2000 #threshold price in dolars for download data from olx
        self._downloadImage = pDownloadImage
        
    def openDriver(self):
        self.driver = self.runBrowserDrive()
        self.openBrowser()
        
    def runBrowserDrive(self):
        assert self._TypeBrowser,"pTypeBrowser is necessary!"
        assert self._browserDrive,"pBrowserDrive is necesaary!"
        opts = Options()
        opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")
        if(self._TypeBrowser=='f'):
            return webdriver.Firefox(self._browserDrive+'chromedriver.exe', options=opts)
            
        elif(self._TypeBrowser=='c'):
            print(self._browserDrive+'chromedriver.exe')
            return webdriver.Chrome(self._browserDrive+'chromedriver.exe', options=opts)
        
    def openBrowser(self):
        self.driver.get(self._olxUrlAutos)
        
    def scrollBrowser(self):
        self.clickButtonLoadMore()
        sleep(random.randint(2, 6))
        
        # go to heading usin smooth scrolling
        self.scrollTop()
        sleep(random.randint(2, 6))
        #to ensure all images has been loaded we go down approximately 20000 px using 
        self.scrollDown()
        sleep(random.randint(2, 6))
        
    def scrollDown(self):
        return self.driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
    
    def scrollTop(self):
        return self.driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
    
    def clickButtonLoadMore(self):
        try:
            #click over cargar mas, waiting 10 seconds while this button was showed
            boton = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@data-aut-id="btnLoadMore"]')))
            boton.click()
            
            #wait 10 seconds til itemPrice was showed
            WebDriverWait(self.driver, 30).until(
                  EC.presence_of_all_elements_located((By.XPATH, '//li[@data-aut-id="itemBox"]//span[@data-aut-id="itemPrice"]'))
                )
        except ElementClickInterceptedException as e:
            log.exception(e)
            
    def runScrap(self, pParallel):
        init = -1
        end  = 0
        while init<=end:
            self.scrollBrowser()
            ads = self.driver.find_elements(by=By.XPATH, value='//li[@data-aut-id="itemBox"]')
            init = end
            end = len(ads)
            ads = ads[init:]
            if(pParallel):
                yield self.applyMultiprocessing(ads)
            else:
                yield self.getData(ads)
            
        
    def applyMultiprocessing(self, ads):
        pool = mp.Pool(mp.cpu_count())

        results = pool.map(self.getDataParallel, [ad for ad in ads])
        
        pool.close()
        
        return results
        
    
            
    def getData(self, pAds):
        print("Amount of  data to download: {}".format(str(len(pAds))))
        listAds = []
        for ad in pAds:
            data = {}
            try:
                # get the price
                precio = ad.find_elements(by=By.XPATH, value='.//span[@data-aut-id="itemPrice"]')
                if(precio!=[]):
                    precio = self.cleanPrice(precio[0].text)
                    if(int(precio)>=self._thresholdPrice):
                        #url detail page
                        url = ad.find_element(by=By.XPATH, value='./a').get_attribute("href")
                        # depiction
                        descripcion = ad.find_element(by=By.XPATH, value='.//span[@data-aut-id="itemTitle"]').text
                        #location
                        lugar = ad.find_element(by=By.XPATH, value='.//span[@data-aut-id="item-location"]').text
                        #Release day
                        diaPublicacion = ad.find_element(by=By.XPATH, value='.//span[@data-aut-id="item-location"]/following-sibling::span').text

                        imageName = 'empty.jpg'
                        if(self._downloadImage):
                            imageName = self.downloadImage(ad)

                        #get details
                        moreData = self.detailAd(url)

                        data['precio']=precio
                        data['descripcion']=descripcion
                        data['lugar'] = lugar
                        data['diaPublicacion'] = diaPublicacion
                        data['imageName'] = imageName
                        data.update(moreData)
                        listAds.append(data)
            except exceptions.StaleElementReferenceException as e:
                log.exception(e)
        return listAds 
    
    def getDataParallel(self, ad):
        data = {}
        try:
            # get the price
            precio = ad.find_elements(by=By.XPATH, value='.//span[@data-aut-id="itemPrice"]')
            if(precio!=[]):
                precio = self.cleanPrice(precio[0].text)
                if(int(precio)>=self._thresholdPrice):
                    #url detail page
                    url = ad.find_element(by=By.XPATH, value='./a').get_attribute("href")
                    # depiction
                    descripcion = ad.find_element(by=By.XPATH, value='.//span[@data-aut-id="itemTitle"]').text
                    #location
                    lugar = ad.find_element(by=By.XPATH, value='.//span[@data-aut-id="item-location"]').text
                    #Release day
                    diaPublicacion = ad.find_element(by=By.XPATH, value='.//span[@data-aut-id="item-location"]/following-sibling::span').text

                    imageName = 'empty.jpg'
                    if(self._downloadImage):
                        imageName = self.downloadImage(ad)

                    #get details
                    moreData = self.detailAd(url)

                    data['precio']=precio
                    data['descripcion']=descripcion
                    data['lugar'] = lugar
                    data['diaPublicacion'] = diaPublicacion
                    data['imageName'] = imageName
                    data.update(moreData)
        except exceptions.StaleElementReferenceException as e:
            log.exception(e)
            return data
        return data
            
    
    def downloadImage(self, ad):
        try:
            url = ad.find_element(by=By.XPATH, value='.//figure[@data-aut-id="itemImage"]/img')
            # I get image url
            url = url.get_attribute('src')
            #we make request the privius url and download data
            image = requests.get(url)
            #get image extension
            extension = image.headers['Content-Type'].split('/')[1]
            # get content as bytes
            image_content = image.content
            # we download image on byte code
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
            #build new name
            name =  str(uuid.uuid4()) + '.'+ extension
            file_path = self._outDir+"/"+ name
            with open(file_path, 'wb') as f:
                image.save(f, extension.upper(), quality=100)
            return name
        except Exception as e:
            log.exception(e)
            return "fail.jpg"
                        
    def detailAd(self, pLink):
        dictDetail = {}
        try:
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[-1]);
            self.driver.get(pLink)
            self.scrollDown()
            WebDriverWait(self.driver, 10).until(
                      EC.presence_of_element_located((By.XPATH, '//div[@data-aut-id="itemParams"]'))
                    )
            moreData = self.driver.find_elements(by=By.XPATH, value='//div[@data-aut-id="itemParams"]/div//div')
            for detail in moreData:
                idDetail=detail.find_elements(by=By.XPATH, value='.//span')[0].text
                detailValue = detail.find_elements(by=By.XPATH, value='.//span')[1].text
                dictDetail[idDetail]=detailValue
            self.closeDriver()
            self.driver.switch_to.window(self.driver.window_handles[0]);
            return dictDetail
        except TimeoutException as e:
            self.closeDriver()
            self.driver.switch_to.window(self.driver.window_handles[0]);
            return dictDetail
    
    def closeDriver(self):
        self.driver.close()
        
    def cleanPrice(self, pPrice):
        #return value on dolars
        #currency exchange $1 == s./ 3.60 
        index = pPrice.lower().find('s/.')
        if(index!=-1):
            return float(pPrice[index+3:].lower().strip().replace(',',''))/3.60
        else:
            index = pPrice.lower().find('$')
            return float(pPrice[index+1:].lower().strip().replace(',',''))


