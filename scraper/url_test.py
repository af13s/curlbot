from lxml import html
import requests
import sys

def htmlTree( URL ):
    page = requests.get(URL)
    tree = html.fromstring(page.content)
    return tree

def url_scraper (tree, urlxpath):
    product_urls = tree.xpath(urlxpath)
    return product_urls

URL = ""
XPATH = ""

while(True):
    print("just press enter to use last url")
    string = input("Enter URL >: ")

    if string == "exit":
        break

    if string:
        URL = string
    
    string = input("Enter xpath >: ")

    if string:
        XPATH = string

    if string == "exit":
        break

    tree = htmlTree(URL)

    product_urls = url_scraper(tree, XPATH)
    
    print("\n", product_urls, "\n")

    
    

# //*[@id="collection-main"]/div[1]/div/div/p[1]/a/@href