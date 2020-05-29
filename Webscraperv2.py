from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

#getting the webpage
def website_setup(websites):
    source_url = requests.get(websites)

    soup = BeautifulSoup(source_url.content, "html.parser")
    return soup

#getting images
def image_search(soup):
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
    return image_url_list
#finding URLS
def url_finder(soup):
    all_urls = [a['href'] for a in soup.find_all('a', href=True)]
    return all_urls
#finding SubHeadings of every article
def sub_heading_finder(soup):
    sub_headings = []
    for tag in soup.find_all(class_="mw-headline"):
        sub_headings.append(tag['id'])
    return sub_headings

#finding citations
def citations_finder(soup):
    citations = []
    citation_div = soup.find(class_="reflist columns references-column-width")
    if citation_div == None:
        pass
    else:
        citation_ol = citation_div.find(class_="references")
        citation_url = citation_ol.find_all('a')
        for y in range(len(citation_url)):
            citations.append(citation_url[y].string)
    return citations
#removing image urls from all_urls
def url_cleaner(all_urls, image_url_list):
    all_urls = [x for x in all_urls if x not in image_url_list]
    return all_urls
#compiling the data into a spreadsheet
def spreadsheet_creator(all_urls, image_url_list, sub_headings, citations, csv_file):
    total_data = {"Urls": all_urls, "Images": image_url_list, "Citations": citations, "SubHeadings":
    sub_headings}
    df = pd.DataFrame.from_dict(total_data, orient = 'index')
    df = df.transpose()
    df.to_csv(csv_file)


#overarching function
def webscraper(websites):
    x = 0
    if isinstance(websites, str) == True:
        csv_file = 'Websv' + str(x) + '.csv'
        soup = website_setup(websites)
        all_urls = url_cleaner(url_finder(soup), image_search(soup))
        spreadsheet_creator(all_urls, image_search(soup), sub_heading_finder(soup), citations_finder(soup), csv_file)
    else:
        for x in range(len(websites)):
            website = websites[x]
            csv_file = 'Websv' + str(x) + '.csv'
            soup = website_setup(website)
            all_urls = url_cleaner(url_finder(soup), image_search(soup))
            spreadsheet_creator(all_urls, image_search(soup), sub_heading_finder(soup), citations_finder(soup), csv_file)
            x = x + 1
