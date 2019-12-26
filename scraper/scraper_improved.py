from lxml import html
import requests
import sys #can be removed when storing directly to database
import os # can also be removed
import pprint
import re
import sys
sys.path.append("..")
from database.database_accessor import database

PRODUCT_TABLE_NAME = "product"

class URLflags:
    def __init__(self, page_flag=None, next_flag=None, limit_flag=None, extra_flags=None):
        self.page_flag = page_flag
        self.next_flag = next_flag
        self.extra_flags = extra_flags
        self.limit_flag = limit_flag

class URLxpaths:
    def __init__(self, product_name=None, product_url=None, product_ingredient_list=None, next_xpath=None, product_img=None):
        self.product_name = product_name
        self.product_url = product_url
        self.next_xpath = next_xpath
        self.product_ingredient_list = product_ingredient_list
        self.product_img_url = product_img

class Retailer:
    def __init__(self, companyname, seedurls, xpathvars, urlflags, baseurl):
        self.company_name = companyname

        self.base_url = baseurl

        self.urls = seedurls

        self.xpaths = URLxpaths(
                        product_name=xpathvars["name"],
                        product_url=xpathvars["url"],
                        product_ingredient_list=xpathvars["ingredients"],
                        next_xpath=xpathvars["next"],
                        product_img=xpathvars["img"]
                    )

        self.urlflags = URLflags(
                        page_flag=urlflags["page"],
                        next_flag=urlflags["next"],
                        limit_flag = urlflags["limit"],
                        extra_flags=urlflags["extra"]
                    )

    def __str__(self):
        return str(self.company_name) + ": " + str(self.base_url)

def htmlTree( URL ):
    page = requests.get(URL)
    tree = html.fromstring(page.content)
    return tree

def normalize_string(string):
    string = re.sub(r'[^\x00-\x7F]+','', string) # remove weird characters
    string = re.sub(r'[^a-zA-Z,]+', ' ', string) # remove numbers and special characters
    string = string.strip().replace("\n", "").replace("\t", "")
    return string

def product_scraper (product_urls, retailer):

    results = []

    for url in product_urls:

        tree = htmlTree(url)

        # print(etree.tostring(tree,pretty_print=True))

        try: 
            
            product_ingredients = tree.xpath(retailer.xpaths.product_ingredient_list)
            product_ingredients = normalize_string(product_ingredients[0]).lower()

            product_name = tree.xpath(retailer.xpaths.product_name)
            product_name = normalize_string(product_name[0])

            product_url = url

        except Exception as e:
            print("Error occured %s", str(e))

        try:
            raise(Exception)
            # add_product_to_db(
            #     brand_name=retailer.company_name,
            #     product_name=product_name,
            #     product_url=product_url,
            #     ingredients=product_ingredients
            # )

        except Exception as e:
            print("\n\n Error occured msg=%s", str(e))
            print("name={}\n ingredients={}\n brand={}\n url={}\n\n".format(product_name, product_ingredients,retailer.company_name, product_url))

        if product_ingredients != "":
            results.append({
                product_name : {
                "product_url": product_url,
                "product_ingredients": product_ingredients,
            }})


    return results

def add_product_to_db(product_name, product_url, ingredients, brand_name, tablename=PRODUCT_TABLE_NAME):
    item = {
        "product_name": product_name,
        "brand_name" : brand_name,
        "product_url": product_url,
        "ingredients": ingredients
    }
    database.add_table_entry(tablename, item)

def url_scraper (tree, urlxpaths):
    product_urls = tree.xpath(urlxpaths.product_url)

    return product_urls


def crawler ( retailer ):

    for url in retailer.urls:

        print(" \n starting url: ", url)

        page_number = 1

        while( True ):

            url += '?'

            if retailer.urlflags.page_flag:
                url += retailer.urlflags.page_flag + "=" + str(page_number)

            if retailer.urlflags.limit_flag:
                url += '&' + retailer.urlflags.limit_flag

            if retailer.urlflags.extra_flags:
                for flag in retailer.urlflags.extra_flags:
                    url += '&' + flag

            # print ("\n Scraping Formatted Url: " , url)
            
            tree = htmlTree (url)

            products = url_scraper(tree, retailer.xpaths)
            products = [retailer.base_url+x for x in products]

            print("total number products: ", len(products))
            print("number successfully scraped: ", len(product_scraper(products, retailer)))

            if (page_number == 1 and retailer.urlflags.next_flag):
                if ( tree.xpath(retailer.xpaths.next_xpath)[0].strip() != retailer.urlflags.next_flag ): #Very Important IF STATEMENT if its the first page there is no prev so next text in first position
                    break														#Femi: Previous line give me an out of range error, like one of the numbers in the IF statement 																#is not an actual index in the list
            else:
                try:
                    if not retailer.xpaths.next_xpath:
                        break
                    if (tree.xpath(retailer.xpaths.next_xpath)[0].strip() != retailer.urlflags.next_flag ): # Every other page should have a nxval in the second position, after previous val second position
                        break
                except IndexError: # On last page there is a previous button but no next button so this is the last page
                    break
            page_number += 1


if __name__ == "__main__":

    consts = open ('constants','r')

    retailers = []
    company = None
    baseurl = None
    seedurls = []

    xpath_template = xpaths = {
        "name" : None,
        "url" : None,
        "ingredients" : None,
        "next": None,
        "img": None
    }

    urlflags_template = urlflags = {
        "page" : None,
        "next": None,
        "limit": None,
        "extra": []
    }

    for line in consts:

        if line[0] == '$':
            print("Adding New Retailer")
            print(seedurls)
            print(xpaths)
            print(urlflags)
            new_retailer = Retailer(company, seedurls, xpaths, urlflags, baseurl)
            retailers.append(new_retailer)
            # print(new_retailer, " added")
            seedurls = []
            company = None
            baseurl = None
            xpath_template = xpaths = {
                "name" : None,
                "url" : None,
                "ingredients" : None,
                "next": None,
                "img": None
            }

            urlflags_template = urlflags = {
                "page" : None,
                "next": None,
                "limit": None,
                "extra": []
            }
            continue
            
        if line[0] == "#" or line.strip() == "":
            continue

        if line[0] == 'x':
            xpath_args = line.split()
            var = xpath_args[0][1:] #get word after x in xarg
            xpaths[var] = xpath_args[1]
            continue

        if line[0] == 's':
            seed_args = line.split()
            seedurls.append(seed_args[1])
        
        if line[0] == '&':
            url_flag_args = line.split()
            var = url_flag_args[0][1:]
            if var != 'extra':
                urlflags[var] = url_flag_args[1]
            else:
                urlflags[var].append(url_flag_args[1])

            continue

        if line[0] == "c":
            company = line.split()[1:]
            company = " ".join(company)
            continue
        
        if line[0] == "b":
            baseurl = line.split()[1]
            continue
    
    consts.close()

    for retailer in retailers:
        # print(retailer)
        crawler(retailer)

