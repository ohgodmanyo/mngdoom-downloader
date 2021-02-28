import requests
from bs4 import BeautifulSoup
import os
import shutil

print('Modules are loaded')

mangaLink = input('Please enter the link to the manga you would like downloading: ')
mangas = input('What mangas would you like downloaded? (x - x) : ')
manga = mangas.split()[0]
manga1 = mangas.split()[2]


def get_links(link):
    chapters_url = requests.get(link)
    soup = BeautifulSoup(chapters_url.text, 'html.parser')
    chapters_html = soup.find('ul', class_='chapter-list')
    chapters_links = chapters_html.find_all('a')
    list_of_chapters = []
    real_list = []
    in_range = False
    for a in chapters_links:
        list_of_chapters.append(a['href'])
    list_of_chapters.reverse()
    for j in list_of_chapters:
        if j.endswith(manga):
            in_range = True
        if in_range:
            real_list.append(j)
        else:
            continue
        if j.endswith(manga1):
            print('Fetched the links')
            return real_list


def get_pages(link):
    pages_html = requests.get('{}/all-pages'.format(link))
    soup = BeautifulSoup(pages_html.text, 'html.parser')
    images = soup.find_all('img')
    image_list = []
    for k in images:
        image_list.append(k['src'])
    print('Fetched the images')
    return image_list


print('Defined functions')

try:
    shutil.rmtree(os.path.realpath(__file__).replace('main.py', 'images'))
    print('Deleted images folder')
except FileNotFoundError:
    print('Images folder not found, creating now')

os.mkdir(os.path.realpath(__file__).replace('main.py', 'images'))
print('Created images folder')

for x in get_links(mangaLink):
    mangaLinkPath = '{}\{}'.format(os.path.realpath(__file__).replace('main.py', 'images'), x.split('/')[-1])
    os.mkdir(mangaLinkPath)
    for n in get_pages(x):
        imgData = requests.get(n).content
        imgLinkPath = n.split('/')[-1]

        with open('{}\{}'.format(mangaLinkPath, imgLinkPath), 'wb') as handler:
            handler.write(imgData)
        print('Finished downloading page {}'.format(imgLinkPath))
    print('Finished downloading manga {}'.format(x.split('/')[-1]))
