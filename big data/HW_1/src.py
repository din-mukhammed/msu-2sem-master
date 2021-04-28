#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import json
from urllib.request import Request, urlopen
from selenium import webdriver


# In[2]:


class GetDataFromCitilink:
    def __init__(self, url):
        self.data = {}
        page = requests.get(url)
        self.soup = BeautifulSoup(page.content, 'html.parser')
        
    def get_data(self):
        title = self.soup.find_all('h1')[0].text.strip().split()
        name = ' '.join(title[2:])
        self.data['Название'] = name
        results = self.soup.find(id='content')
        if results is None:
            return {}
        full_specs = results.find_all('div', class_='SpecificationsFull')
        for specs in full_specs:
            spec = specs.find('div', class_='Specifications')
            if spec is None:
                continue
            for res in spec:
                x = res.find('div', class_ = 'Specifications__column Specifications__column_name')
                y = res.find('div', class_ = 'Specifications__column Specifications__column_value')
                if x is None or y is None:
                    continue
                key, val = x.text.replace('\n', '').strip(), y.text.replace('\n', '').strip() 
                self.data[key] = val
        return self.data


# In[3]:


class GetDataFromDns:
    def __init__(self, url):
        self.data = {}
        chromedriver_path = 'C:\\Users\\dimas\\Downloads\\chromedriver_win32\\chromedriver.exe'
        options = webdriver.ChromeOptions()
        options.add_argument('headless')  # для открытия headless-браузера
        driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=options)
        driver.get(url)
        html = driver.page_source
        self.soup = BeautifulSoup(html, 'html.parser')
        driver.quit()
        
    def get_data(self):
        name = self.soup.find('div', class_ = 'price_item_description').text.split()
        name = ' '.join(name[2:])
        self.data['Название'] = name
        tabs = self.soup.find('div', class_ = 'product-card-tabs__contents')
        table = tabs.find('table')
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            if len(cols) < 2:
                continue
            self.data[cols[0]] = cols[1]
        return self.data


# In[21]:


def get_data_from_citilink(input_txt, output_json):
    urls, objs, features, output = [], [], [], []
    with open(input_txt, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.replace('\n', '')
            urls.append(line)
    for url in urls:
        obj = GetDataFromCitilink(url)
        objs.append(obj.get_data())
    for obj in objs:
        features.append(set(obj.keys()))
    main_features = features[0]
    for feature in features:
        main_features &= feature
    for obj in objs:
        obj_copy = obj.copy()
        for obj_feature in obj:
            if obj_feature not in main_features:
                del obj_copy[obj_feature]
        output.append(obj_copy)
    with open(output_json, 'w') as out_file:
        for x in output:
            json_obj = json.dumps(x, ensure_ascii=False, indent=2)
            out_file.write(json_obj + '\n')


# In[4]:


def get_data_from_dns(input_txt, output_json):
    urls, objs, features, output = [], [], [], []
    with open(input_txt, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.replace('\n', '')
            urls.append(line)
    for url in urls:
        obj = GetDataFromDns(url)
        objs.append(obj.get_data())
    with open(output_json, 'w') as out_file:
        for x in objs:
            json_obj = json.dumps(x, ensure_ascii=False, indent=2)
            out_file.write(json_obj + '\n')


# In[23]:


get_data_from_citilink(input_txt='data_citilink.txt', output_json='citilink.json')


# In[6]:


get_data_from_dns(input_txt='data_dns.txt', output_json='dns.json')

