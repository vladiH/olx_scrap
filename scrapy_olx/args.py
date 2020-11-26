# coding: utf-8
'''pTypeBrowser = 'c'
pBrowserDrive = './modules/'
pOlxUrlAutos = 'https://www.olx.com.pe/vehiculos_c362'
pOutDir = './salida'
pDownloadImage=False
runScrap(pTypeBrowser, pBrowserDrive, pOlxUrlAutos, pOutDir, pDownloadImage) '''
import argparse
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
                    help="True for download images else False", action='store_false', dest='img', default=False)

args = parser.parse_args()

print(args)
pTypeBrowser = 'c'
pBrowserDrive = './modules/'
pOlxUrlAutos = 'https://www.olx.com.pe/vehiculos_c362'
pOutDir = './salida'
pDownloadImage=False
runScrap(pTypeBrowser, pBrowserDrive, pOlxUrlAutos, pOutDir, pDownloadImage)