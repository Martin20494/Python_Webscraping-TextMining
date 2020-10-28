import os
import re
import requests
from bs4 import BeautifulSoup

mainweb = 'https://www.nzherald.co.nz/nzh-search/NZH/pollutant/'
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
page_start = 1
page_end = 51

def webpage(mainweb, page_start, page_end):
    '''Getting webpage'''
    list_results = []
    for num in range(page_start, page_end):
        url = mainweb + str(num) +'/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all(class_= 'result-item')
        list_results.append(results)
    return list_results

def getlink(links):
    '''Getting links from webpage'''
    list_link = []
    for lin in links:
        link = str(lin.a['href'])
        list_link.append('https://www.nzherald.co.nz/' + link)
    return list_link

def extract_set_link(list_results):
    '''Extracting set of links from list of results'''
    new_url_list = []
    for results in list_results:
        new_url_list += getlink(results)
    return new_url_list
          
     
def gettext(new_url):
    '''Extracting all texts from NZHerald'''
    response = requests.get(new_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find(id= 'article-content')
    text = ''
    try:
        links = results.find_all('p')
        if len(results.findAll('br')) > 1:
            text += links[0].contents[0].strip() + '\n'
            for i in range(len(links)):
                for num in range(1, len(links[i].findAll('br')), 2):
                    try:
                        text += links[i].findAll('br')[num].nextSibling.strip() + '\n'
                    except TypeError:
                        pass
                    except IndexError:
                        pass
        else:
            for link in links:
                try:
                    text += link.contents[0].strip() + '\n'
                except TypeError:
                    pass
                except IndexError:
                    pass
    except AttributeError:
        pass
    except TypeError:
        pass
    return text

def getdate(new_url):
    '''Extracting the date'''
    response = requests.get(new_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    dates = soup.find('div', class_='publish')
    if dates != None:
        date_text = ''
        for char in dates.contents[0]:
            if char not in punctuations:
                date_text += char
        return date_text.replace(' ', '')
    else:
        pass
    
def getname(new_url):
    '''Ectracting name of link'''
    response = requests.get(new_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    names = soup.find('h1')
    if names != None:
        name = ''
        name_text= ''
        if names.contents[0].strip() != '':
            name += names.contents[0]
        else:
            if names.em != None:
                name += names.em.contents[0][:-1] + ' '
                name += names.contents[2].strip()
            else:
                pass
        for char in name:
            if char not in punctuations:
                name_text += char
        return name_text
    else:
        pass

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
        os.chdir('P:\Courses\DIGI405 - Text and Discourse\Assigment1\Corpus\Total - Data') #change the directory into another folder
        date = getdate(new_url)
        text = gettext(new_url)
        name = getname(new_url)
        txtfile(text, date, name)
        
def main():
    '''Scraping'''
    result = webpage(mainweb, page_start, page_end)
    links = extract_set_link(result)
    all_file(links)    