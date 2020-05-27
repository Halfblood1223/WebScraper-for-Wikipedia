from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

#getting the webpage
source_url = requests.get(input("Website Link: "))

soup = BeautifulSoup(source_url.content, "html.parser")
soup.prettify()

#getting images
x = 0
image_url_list = []

#all the image containers
all_imagediv = soup.find_all("div", class_="thumbinner")

#searching through each individual container
for i in range(len(all_imagediv)):
    image_div = all_imagediv[x]
    image_url = image_div.a["href"]
    #append the resulting image url to a list
    image_url_list.append(image_url)
    x = x + 1
#finding URLS
all_urls = [a['href'] for a in soup.find_all('a', href=True)]

#finding SubHeadings of every article
sub_headings = []
for tag in soup.find_all(class_="mw-headline"):
    sub_headings.append(tag['id'])

#finding citations
citations = []
citation_div = soup.find(class_="reflist columns references-column-width")
if citation_div == None:
    pass
else:
    citation_ol = citation_div.find(class_="references")
    citation_url = citation_ol.find_all('a')
    for y in range(len(citation_url)):
        citations.append(citation_url[y].string)

#compiling the data into a spreadsheet
total_data = {"Urls": all_urls, "Images": image_url_list, "Citations": citations}
df = pd.DataFrame.from_dict(total_data, orient = 'index')
df = df.transpose()
df.to_csv('Websv2.csv')
