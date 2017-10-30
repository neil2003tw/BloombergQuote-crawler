import urllib3
import certifi
import csv
from datetime import datetime as dt
from bs4 import BeautifulSoup

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where()
    ) # Verifies certificates when making requests

list_pages=['https://www.bloomberg.com/markets/stocks/world-indexes/americas',
           'https://www.bloomberg.com/markets/stocks/futures',
           'https://www.bloomberg.com/markets/stocks/world-indexes/europe-africa-middle-east',
           'https://www.bloomberg.com/markets/stocks/world-indexes/asia-pacific']
stock_list=[]
for list_page in list_pages:
    response=http.request('GET',list_page)
    soup = BeautifulSoup(response.data,'lxml')
    cat_name_box=soup.find('h1',attrs={'class':'title-box__name'})
    stock_list_box = soup.find_all('div', attrs={'data-type':'abbreviation'})
    current_list=[[cat_name_box.text,x.text.strip()] for x in stock_list_box]
    stock_list=stock_list+current_list
    print('Crawler status: Done with '+list_page.split('/')[-1]+' list.')

stock_data=[]
for stock_cat,stock_id in stock_list[1:5]:
    if ' ' in stock_id:
        stock_id = stock_id.replace(' ','%20') # Prevent space in url
    quote_page = 'https://www.bloomberg.com/quote/'+stock_id
    response=http.request('GET',quote_page)
    soup = BeautifulSoup(response.data,'lxml')

    name_box = soup.find('h1', attrs={'class':'name'})
    name=name_box.text.strip() #Get Stock Name

    price_box = soup.find('div', attrs={'class':'price'})
    price = price_box.text #Get Stock Price

    stock_data.append([stock_cat,name,price])
    print('Crawler status: Done with ' + stock_id + ' in '+stock_cat+'.')

with open('stock_data.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)
    for stock_cat, name, price in stock_data:
        writer.writerow([stock_cat, name, price, dt.now()])
        