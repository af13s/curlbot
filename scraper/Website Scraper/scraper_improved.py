from lxml import html
import requests
import sys #can be removed when storing directly to database
import os # can also be removed

class URLflags:
    def __init__(self, page_flag=None, next_flag=None, limit_flag=None, extra_flags=None):
        self.page_flag = page_flag
        self.next_flag = next_flag
        self.extra_flags = extra_flags

class URLxpaths:
    def __init__(self, product_name, product_url, product_ingredient_list, next_xpath=None):
        self.product_name = product_name
        self.product_url = product_url
        self.next_xpath = next_xpath
        self.product_ingredient_list = product_ingredient_list

class Retailer:
    def __init__(self, companyname, seedurls, xpathvars, urlflags):
        self.company_name = companyname

        self.urls = seedurls

        self.xpaths = URLxpaths(
                        product_name=xpathvars["xname"],
                        product_url=xpathvars["xurl"],
                        product_ingredient_list=xpathvars["xingredients"],
                        next_xpath=xpathvars["xnext"]
                    )

        self.urlflags = URLflags(
                        page_flag=urlflags["page"],
                        next_flag=urlflags["next"],
                        limit_flag = urlflags["limit"],
                        extra_flags=urlflags["extra"]
                    )

        def __str__(self):
            return str(self.company_name)

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

            print(products, "\n\n")

            # Product_Scraper(products["product_urls"], retailer.xpaths)

            if (page_number == 1 and retailer.urlflags.next_flag):
                if ( tree.xpath(retailer.xpaths.next_xpath)[0].strip() != retailer.urlflags.next_flag ): #Very Important IF STATEMENT if its the first page there is no prev so next text in first position
                    break														#Femi: Previous line give me an out of range error, like one of the numbers in the IF statement 																#is not an actual index in the list
            else:
                try:
                    if (tree.xpath(retailer.xpaths.next_xpath)[0].strip() != retailer.urlflags.next_flag ): # Every other page should have a nxval in the second position, after previous val second position
                        break
                except IndexError: # On last page there is a previous button but no next button so this is the last page
                    break
            page_number += 1



if __name__ == "__main__":

    consts = open ('constants','r')

    retailers = []
    company = None
    seedurls = []
    xpaths = {}
    urlflags = {}

    for line in consts:

        if line[0] == '$':
            print("Adding New Retailer")
            print(seedurls)
            print(xpaths)
            print(urlflags)
            new_retailer = Retailer(company, seedurls, xpaths, urlflags)
            retailers.append(new_retailer)
            print(new_retailer, " added")
            seedurls = []
            xpaths = {}
            urlflags = {}
            continue
            
        if line[0] == "#" or line.strip() == "":
            continue

        if line[0] == 'x':
            xpath_args = line.split()
            var = xpath_args[0][1:]
            xpaths[var] = xpath_args[1]
            continue

        if line[0] == 's':
            seed_args = line.split()
            seedurls.append(seed_args[1])
        
        if line[0] == '&':
            url_flag_args = line.split()
            var = url_flag_args[0][1:]
            urlflags[var] = url_flag_args[1]
            continue
    
    consts.close()

    for retailer in retailers:
        Crawler(retailer)

