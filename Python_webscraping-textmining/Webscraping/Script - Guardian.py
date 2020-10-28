import os
import re
import requests
from bs4 import BeautifulSoup

mainweb = 'https://www.theguardian.com/environment/pollution?page='
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
page_start = 1
page_end = 51

def webpage(mainweb, page_start, page_end):
    '''Getting webpage'''
    list_results = []
    for num in range(page_start, page_end):
        url = mainweb + str(num)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', class_='fc-item__content')
        list_results.append(results)
    return list_results

def getlink(links):
    '''Getting links from webpage'''
    list_link = []
    for lin in links:
        link = str(lin.a['href'])
        list_link.append(link)
    return list_link

def extract_set_link(list_results):
    '''Extracting set of links from list of results'''
    new_url_list = []
    for results in list_results:
        new_url_list += getlink(results)
    return new_url_list

def gettext(new_url):
    response = requests.get(new_url)
    soup = BeautifulSoup(response.text, 'html.parser')    
    results = soup.find('div', class_= 'content__article-body')
    text = ''
    try:
        links = results.find_all('p')
        for link in links:
            try:
                if isinstance(link.contents[0], str):
                    text += link.contents[0] + '\n'
                elif isinstance(link.contents[1], str) and len(link.contents[1].strip()) > 1:
                    text += link.contents[1] + '\n'
                else:
                    text += link.contents[3] + '\n'
            except TypeError:
                pass   
    except AttributeError:
        pass
    except IndexError:
        pass
    return text

def getdate(new_url):
    response = requests.get(new_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    date_text = ''
    try:
        date = soup.find('time')
        date_text = date.contents[0].strip()[4:]
    except AttributeError:
        pass
    return date_text.replace(' ', '')

def getname(new_url):
    response = requests.get(new_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title_text = ''
    try:
        title1 = soup.find('h1', class_='content__headline')
        title2 = title1.contents[0].strip()
        for char in title2:
            if char not in punctuations:
                title_text += char
    except AttributeError:
        pass
    return title_text  

def txtfile(text, date, name):
    '''Writing text into txt file'''
    if text != '':
        name = date + '_' + name + '.txt'
        file = open(name, 'w', encoding='utf8')
        file.write(text.strip())
        file.close()
    else:
        pass
    

def all_file(new_url_list):
    '''Combining all files'''
    for num, new_url in enumerate(new_url_list, 1):
        print(new_url, num)
        os.chdir(r'/Users/thongnguyen/Desktop/UC courses/DIGI405 - Text Mining/Assignment/Corpus 5 - Guardian') #change the directory into another folder
        date = getdate(new_url)
        text = gettext(new_url)
        name = getname(new_url)
        txtfile(text, date, name)
        
def main():
    '''Scraping'''
    result = webpage(mainweb, page_start, page_end)
    links = extract_set_link(result)
    all_file(links)