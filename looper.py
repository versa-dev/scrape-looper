import pandas as pd
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re

origin_url = 'https://www.looper.com/'
later_url = 'https://www.looper.com/?ajax=1&offset=27&action=more-stories&featured%5B%5D=202503&featured%5B%5D=201979&featured%5B%5D=201091'
offset = 17
end = 1

# get articles from the urls
def getArticles(url):
    category = []
    author = []
    title = []
    article_url = []
    flag = 1
    try:
        html = urlopen(url)
    except:
        flag = 0
        return category, author, title, article_url, flag
    bsObject = BeautifulSoup(html.read())
    article_list = bsObject.findAll('article', {'class':'article-block'})
    for item in article_list:
        category.append(item.find('span',{'class':'category'}).text)
        author.append(item.find('span',{'class':'author'}).text[1:])
        title.append(item.find('h3').text)
        article_url.append(item.find('h3').find('a', attrs={'href': re.compile("^https://")}).get('href'))
    #print(category, author, title, article_url, flag)
    return category, author, title, article_url, flag

# get content of articles from the article urls
def getContent(url):
    title = []
    content = []
    try:
        html = urlopen(url)
    except:
        return ("There is no content for this article.")
    bsObject = BeautifulSoup(html.read())
    date = bsObject.find('span',{'class':'byline-timestamp'}).text[1:]
    content_list = bsObject.findAll('div',{'class':'news-article'})
    title.append(content_list[0].find('h1').text)
    des = ''
    for item in content_list[0].findAll('p'):
        des = des + item.text
    content.append(des)
    for item in content_list[1:]:
        title.append(item.find('h2').text)
        content.append(item.find('div', {'class':'columns-holder'}).text[1:])
        des1 = ''
        for text in item.findAll('p'):
            des1 = des1 + text.text
        content.append(des1)
    json = {}
    for ind in range(len(title)):
        json[title[ind]] = content[ind]
    return json, date
#getContent('https://www.looper.com/203681/why-princess-yue-from-the-last-airbender-looks-so-familiar/')

step = -1
categories = []
titles = []
dates = []
contents = []
authors = []
while(end == 1):
    if step == -1:
        url = origin_url
    else:
        url = 'https://www.looper.com/?ajax=1&offset=' + str(27+18*step) + '&action=more-stories&featured%5B%5D=202503&featured%5B%5D=201979&featured%5B%5D=201091'
    step = step + 1
    category, author, title, article_url, flag = getArticles(url)
    end = flag
    for ind in range(len(category)):
        content, date = getContent(article_url[ind])
        categories.append(category[ind])
        titles.append(title[ind])
        dates.append(date)
        authors.append(author[ind])
        contents.append(content)
dict = {'title':titles, 'author':authors, 'date':dates, 'category':categories, 'content':contents}        
out = pd.DataFrame(dict)     
out.to_csv('looper.csv')