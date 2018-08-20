import requests
import json
from selenium import webdriver
from time import sleep
import os
from selenium.webdriver.chrome.options import Options
import urllib
import math
import csv

class Shopee :
    cookie = ""
    token = ""
    sellerid = ""
    sellername = ""
    path = ""
    catid = []
    itemid = []
    data = []

    def __init__(self, name, path) :
        self.sellername = name
        self.path = path
        
    def getCookie(self) :
        url = "https://shopee.co.id/"
        co = Options()
        co.add_argument("--nosandbox")
        dp = os.getcwd()+"\\chromedriver.exe"
        driver = webdriver.Chrome(executable_path = dp, chrome_options = co)
        driver.get(url)
        self.cookie = ';'.join(['{}={}'.format(item['name'], item['value'])
                    for item in driver.get_cookies()])
        self.token = driver.get_cookie('csrftoken')['value']          
        driver.quit()

    def getSellerId(self) :
        data = {'usernames':[self.sellername]}
        url = "https://shopee.co.id/api/v1/shop_ids_by_username/"
        headers = {'x-csrftoken': self.token,
                   'cookie': self.cookie,
                   'content-type': 'application/json',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                   'referer': 'https://shopee.co.id/'
                   }
        req = requests.post(url, data=json.dumps(data), headers=headers)
        res = req.json()
        self.sellerid = res[0][self.sellername]

    def getCatId(self) :
        url = "https://shopee.co.id/api/v1/shop_collections/?filter_empty=1&limit=20&offset=0&shopid={}".format(self.sellerid)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        req = requests.get(url, headers=headers)
        res = req.json()
        for val in res :
            self.catid.append(val['shop_collection_id'])

    def getItemId(self, catid) :
        url = "https://shopee.co.id/api/v2/search_items/?by=pop&limit=30&match_id={}&newest=0&order=desc&page_type=shop&shop_categoryids={}".format(self.sellerid, catid)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        req = requests.get(url, headers=headers)
        res = req.json()
        for val in res['items'] :
            self.itemid.append(val['itemid'])

    def getItemInfo(self, itemid) :
        url = "https://shopee.co.id/api/v1/item_detail/?item_id={}&shop_id={}".format(itemid, self.sellerid)
        headers = {'x-csrftoken': self.token,
                   'cookie': self.cookie,
                   'referer': 'https://shopee.co.id/',
                   'x-api-source': 'pc',
                   'accept': '*/*',
                   'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
                   'accept-encoding': 'gzip, deflate, br',
                   'x-requested-with': 'XMLHttpRequest',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        req = requests.get(url, headers=headers)
        data = req.json()
        datas = {'ps_product_name': data['name'],
                 'ps_product_description': data['description'],
                 'ps_price': data['price'],
                 'ps_stock': data['stock'],
                 'ps_days_to_ship': data['estimated_days'],
                 'ps_brand': data['brand'],
                 'ps_catid': data['catid'],
                 'ps_sub_catid': data['sub_catid'],
                 'ps_third_catid': data['third_catid'],
                 'images': [],
                 'models': [],
                 'hashtag': data['hashtag_list']
                }

        images = data['images'].split(",")
        for val in images :
            datas['images'].append("https://cf.shopee.co.id/file/{}".format(val))

        for val in data['models'] :
            if val['stock'] != 0 :
                datass = {'stock': val['stock'], 'name': val['name'], 'price': val['price']}
                datas['models'].append(datass)
            
        self.data.append(datas)

    def exe(self) :
        self.getCookie()
        self.getSellerId()
        self.getCatId()
        if self.catid not None :
            for i in self.catid :
                self.getItemId(i)

        if self.itemid not None :
            for j in self.itemid :
                self.getItemInfo(j)
                
shopee = Shopee("suprashop", "D:/ggg")
