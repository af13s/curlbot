from lxml import html
import requests
import sys #can be removed when storing directly to database
import os # can also be removed

class URLflags:
    def __init__(self, page_flag=None, next_flag=None, limit_flag=None, extra_flags=None):
        self.page_flag = page_flag
        self.next_flag = next_flag
        self.extra_flags = extra_flags # list

class URLxpaths:
    def __init__(self, product_name, product_url, product_ingredient_list, next_xpath):
        self.product_name = product_name
        self.product_url = product_url
        self.next_xpath = next_xpath
        self.product_ingredient_list = product_ingredient_list

class RetailerObj:
    def __init__(self, seedurls, xpathvars, urlflags): #change nextpgxpath to go into the object, change flags to take pgincn nxval and extras
        self.urls = seedurls       # Www.example.com
        self.xpaths = URLxpaths(product_name=xpathvars[0],product_url=xpathvars[1], product_ingredient_list=xpathvars[2], next_xpath=xpathvars[3])     # name,url,price,image
        self.urlflgs = URLflags(page_flag=urlflags["page"], next_flag=urlflags["next"], limit_flag = urlflags["limit"], extra_flags=urlflags["extra"])    # flags : PageID, NextID, ExtraFlgs

def htmlTree( URL ):
    page = requests.get(URL)
    tree = html.fromstring(page.content)
    return tree

def Product_Scraper (product_urls, urlxpaths):

    for url in product_urls:

        results = {}

        tree = htmlTree(url)

        # print(etree.tostring(tree,pretty_print=True))

        product_ingredients = tree.xpath(urlxpaths.product_ingredient_list)
        product_name = tree.xpath(urlxpaths.product_name)
        product_url = url

        results[product_name] = {
            "product_url": product_url,
            "product_ingredients": product_ingredients
        }


    return results

def URL_Scraper (tree, urlxpaths):
    product_urls = tree.xpath(urlxpaths.product_urls)
    return product_urls


def Crawler ( retailer ):

    for url in retailer.urls:

        print("starting url:", url)

        page_number = 1

        while( True ):

            url += '?'

            if retailer.urlflags.page_flag:
                url += retailer.urlflags.page_flag

            if retailer.urlflags.limit_flag:
                url += '&' + retailer.urlflags.limit_flag

            if retailer.urlflags.extra_flags:
                for flag in retailer.urlflags.extra_flags:
                    url += '&' + flag

            print ("Scraping Formatted Url: " , url)
            
            tree = htmlTree (url)

            products = URL_Scraper(url, retailer.xpaths)

            Product_Scraper(products["product_urls"], retailer.xpaths)

            if (pnum == 1):
                if ( tree.xpath(retailer.xpaths.next_xpath)[0].strip() != retailer.urlflgs.next_flag ): #Very Important IF STATEMENT if its the first page there is no prev so next text in first position
                    break														#Femi: Previous line give me an out of range error, like one of the numbers in the IF statement 																#is not an actual index in the list
            else:
                try:
                    if (tree.xpath(retailer.xpaths[4])[0].strip() != retailer.urlflgs[1] ): # Every other page should have a nxval in the second position, after previous val second position
                        break
                except IndexError: # On last page there is a previous button but no next button so this is the last page
                    break
            pnum += 1




consts = open ('Constants.txt','r')

