
# coding: utf-8

# In[ ]:


#!pip install selenium #scrap
#!pip install requests #http request
#!pip install keyboard #user key board detection
#!pip install psycopg2 #postgresql driver
#!pip install sqlalchemy #ORM for postgresql
#!pip install yaml  #yaml file
#!pip install pandas #data structuring on tables and data management
#!pip install Pillow #image management library
#!pip install multiprocessing #to run code on parallel behavior


# In[ ]:


import argparse
import sys
import logging
import pandas as pd
from modules import setup_environment
from modules import olx_scrapy
import sqlalchemy


# In[ ]:


log = logging.getLogger(__name__)


# In[ ]:


def readParams():
    parser = argparse.ArgumentParser(description='Extract data from olx, auto section.')
    
    parser.add_argument('op', type=str, choices=['run','show'], 
                   help='run:to start get data from internet, show:to show the previous save data')
    
    parser.add_argument('--url',  type=str,
                        help="enter url from OLX, section autos")
    
    parser.add_argument('-tb','--pTypeBrowser', dest='tb',  type=str, choices=['f','c'],
                        default='c',
                        help="enter f if you have firefox or c if you have chrome")

    parser.add_argument('-bd','--pBrowserDrive', dest='bd',  type=str,  metavar=['chromedriver', 'geckodriver'], help="enter browser driver path", default='./modules/')

    parser.add_argument('-out','--pOutDir',  type=str,
                        help="enter output directory path for images", default='./salida')

    parser.add_argument('-img', '--pDownloadImage',
                        help="True for download images else False", 
                        action='store_false', dest='img', default=False)

    args = parser.parse_args()
    
    return args


# In[ ]:


def fixData(ad):
    aux = ad.copy()
    for key, val  in list(aux.items()):
        if(key.lower()=='diapublicacion'):
            ad['dia_publicacion']=ad.pop(key)
        elif(key.lower()=='imagename'):
            ad['imagen']=ad.pop(key)
        elif(key.lower()=='año'):
            ad['anno']=ad.pop(key)
        elif(key.lower()=='condición'):
            ad['condicion']=ad.pop(key)
        elif(key.lower()=='transmisión'):
            ad['transmision']=ad.pop(key)
        elif(key.lower()=='tipo de vendedor'):
            ad['tipo_vendedor']=ad.pop(key)
        else:
            ad[key.lower()]=ad.pop(key)
    if('descripcion' in ad):
        ad.pop('descripcion')
    if('tipo' in ad):
        ad.pop('tipo')
    return ad


# In[ ]:


def saveData(engine, ads):
    for ad in ads:
        print(ad)
        try:
            ad = fixData(ad)  
            query = "insert into autos ({keyTuple}) values {valTuple}".format(keyTuple=",\n ".join(ad), valTuple=tuple(ad.values()))
            engine.execute(query);
        except sqlalchemy.exc.ProgrammingError as e:
            log.exception(e)


# In[ ]:


def readData():
    engine = setup_environment.get_database()
    con = engine.raw_connection()
    try:
        df_models = pd.read_sql('select * from autos;', con=con)
        print(df_models)
        return df_models
    except:
        log.exception('Unexpected error')
    finally:
        con.close()


# In[ ]:


def runScrap(pTypeBrowser, pBrowserDrive, pOlxUrlAutos, pOutDir, pDownloadImage):
    engine = setup_environment.get_database()
    scrap = olx_scrapy.SeleniumScrapy(pTypeBrowser, pBrowserDrive, pOlxUrlAutos, pOutDir, pDownloadImage)
    scrap.openDriver()
    ads = scrap.runScrap(pParallel=False)
    con = engine.connect()
    for ad in ads:
        saveData(con, ad)    
    scrap.closeDriver()
    con.close()


# In[ ]:


def main():
    args = readParams()
    if(args.op== 'show'):
        pd_data = readData()
        pd_data.to_csv(args.pOutDir+'/olx.csv')
    if(args.op == 'run'):
        assert args.url != None, 'url  is required!'
        runScrap(args.tb, args.bd, args.url, args.pOutDir, args.img)


# In[ ]:


main()


# In[ ]:


#pTypeBrowser = 'c'
#pBrowserDrive = './modules/'
#pOlxUrlAutos = 'https://www.olx.com.pe/vehiculos_c362'
#pOutDir = './salida'
#pDownloadImage=True
#runScrap(pTypeBrowser, pBrowserDrive, pOlxUrlAutos, pOutDir, pDownloadImage)

