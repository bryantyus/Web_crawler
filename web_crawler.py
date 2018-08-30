import requests
import sys
from bs4 import BeautifulSoup
import shutil
import os


# with open(sys.argv[1], "r") as fp:
    # url = fp.readline().strip()
# read url from data.

def fetch_img_of_ptt(url):
    req = requests.get(url)
# print(req.status_code)
    soup = BeautifulSoup(req.text, 'lxml')
    lt = []
    for img in soup.find_all(rel = 'nofollow'):
        if(('.jpg' or '.png') in img.get_text()):
            lt.append(img.get_text())
#  done .
    for img in lt:
        filename = img.split('/')[-1]
        res = requests.get(img, stream = True)
        with open(filename, "wb") as fp:
            shutil.copyfileobj(res.raw, fp) # res.raw : src, fp : dst
            del res


def craw_page(start_page): #start_page is the url of a web page
    req = requests.get(start_page)
    soup = BeautifulSoup(req.text, 'lxml')
    global dir_num

    for item in soup.find_all('a'):
        # then get all url.
        web = item.get('href')
        if not web :
            continue
        if 'M' in web.split('/')[-1].split('.')[0]:
            pathname = './dir' + str(dir_num)
            dir_num+=1
            if(os.path.isdir(pathname)):
                shutil.rmtree(pathname)
            os.mkdir(pathname)
            os.chdir(pathname)

            fetch_img_of_ptt('https://www.ptt.cc'+web)

            os.chdir('../')

    for item in soup.find_all('a'):
        get_class = item.get('class')
        if get_class:
            if ('btn' and 'wide') in get_class:
                next_page = item.get('href')
                if next_page:
                    next_page_number = next_page.split('/')[-1].split('.')[0].strip('index')
                    if next_page_number:
                        next_page_number = int(next_page_number)
                        if next_page_number > 1:
                            return 'https://www.ptt.cc'+next_page

        # if ('btn' and 'wide') in next_page:
            # print(next_page)
# fetch_img_of_ptt('https://www.ptt.cc/bbs/Beauty/M.1535070282.A.BAB.html')

next = ''
dir_num = 1
next = craw_page('https://www.ptt.cc/bbs/Beauty/index.html')
for i in range(3):
    if next:
        next = craw_page(next)

# craw next page.
