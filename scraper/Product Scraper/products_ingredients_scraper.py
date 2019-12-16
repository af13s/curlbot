################## FLIGHTCLUB SCRAWLER ######################

## IMPORTS ##
import lxml.etree as etree
from lxml import html
import requests
import json
import csv

import sys #can be removed when storing directly to database
import os # can also be removed

allShoes = {}

########################################## FUNCTIONS ####################################################################

# parse html request and get get tree structure for xpath searching
def htmlTree( URL ):
    page = requests.get(URL)
    tree = html.fromstring(page.content)
    return tree

##def getSizes(shoe):
##	tree = htmlTree(shoe.URL)
##    shoe.sizes = (tree.xpath(sizexpath))

##def getPrice(shoe):
##		pricexpath = ""
##		for size in shoe.sizes:
##		tree = htmlTree(shoe.URL)
##		for sizes in shoe.sizes
##       pricexpath = tree.getpath(r)  #make sure to only return value that exactly matches string #test amout of values returned
##		shoe.price.append(tree.xpath(pricexpath)) #test the correctness of the returned value

# Scrape Given URL to extract fields
def Scraper (url, xpaths):

    tree = htmlTree(url)

    # print(etree.tostring(tree,pretty_print=True))

    # This will extract a list of shoe names on page
    product_ingredients = (tree.xpath(xpaths[1]))
    exact_productname = (tree.xpath(xpaths[0]))

    results = {}

    for i in range (len(exact_productname)): #iterate through all shoe listings on page
            try:
                print()
                print("product: {}".format(exact_productname[i]))
                print("ingredients: {}".format(product_ingredients[i]))
                print()
                results[str(exact_productname[i].strip())] = product_ingredients[i]
            except IndexError:
                print("OUT OF RANGE ITEM")

    return results


#################################### FUNCTIONS ##################################################################
if __name__ == "__main__":

    try:
        os.remove("ingredients.txt")
    except FileNotFoundError:
        pass

    shop = open ('shop_list.txt','r') #open retailers list

    sephore_xpath = ['//*[@id="tabpanel2"]/div/b/text()','//*[@id="tabpanel2"]/div/text()'] # will load from file in the future
    fenty_xpath = ['//*[@id="ui-id-4"]/div/p/strong' , '//*[@id="ui-id-4"]/div/p/strong/text()']

    xpaths = [sephore_xpath, fenty_xpath]

    products = {}

    for line in shop:
        if line[0] == "#":
            continue
        products[line] = {}

    shop.close() #close list of retailers

    for url in products:
        products[url] = Scraper(url , xpaths[0])


    save = json.dumps(products,sort_keys=True, indent=4)

    orig_sys = sys.stdout #saving output stream
    ingredients_out = open('ingredients.json', 'w')
    sys.stdout = ingredients_out #redirecting output to output file shoelist.txt
    print(save)
    sys.stdout = orig_sys

    with open('ingredients.csv', 'w') as file:  # Just use 'w' mode in 3.x
        out = csv.DictWriter(file, products.keys())
        out.writeheader()
        out.writerow(products)
