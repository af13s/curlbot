import boto3
import os
import itertools
import pprint
import re
import sys
from tqdm import tqdm
sys.path.append("..")
import dialogflow_accessor
from database.database_accessor import database as db
from random import randint, seed
from datetime import datetime
import time
seed(datetime.now())

pp = pprint.PrettyPrinter(indent=4)

AWS_ACCESS_KEY_ID =os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
REGION_NAME='us-west-1'


MATCH_WINDOW = 3
MINIMUM_SIGNIFICANT_KEYWORDS = 4

DEFAULT_SEARCH_PHRASES = [
    "Search for",
    "Look up",
    "Find",
    "look for",
    "please find",
    "try",
    "tell me about",
    "I'd like to know about",
    "analyze",
    "can you do"
]


PRODUCT_TYPE_SET = {
    "shampoo",
    "conditioner",
    "milk",
    "smoothie",
    "mist",
    "bar",
    "masque",
    "gel",
    "leave-in",
    "clay",
    "cream",
    "treatment",
    "detangler",
    "mud",
    "rinse",
    "soap",
    "serum",
    "moisturizer",
    "elixir",
    "fragrance",
    "cleanser",
    "spray",
    "custard",
    "foam",
    "scrub",
    "butter",
    "spritz",
    "gelee",
    "pudding",
    "oil",
}

## TODO

# Create entities of type $(brand_name)+Product with this script
# Update the entities by using the product name gotten from the database and the product name
# Whe querying for a product use the brand_name to search in the appropriate entity

# add product normalizer function to remove special chars formatting etc

def get_brand_names():
    database = db.dynambo_admin_client()

    results = database.scan(
        TableName="product",
        AttributesToGet=[
            "product_name",
            "brand_name"
        ],
    )

    products = {}

    for result in results["Items"]:
        company_name = result["brand_name"]['S']
        #temporary code until database is wiped
        company_name = company_name.replace("_", " ")
        if company_name not in products:
            products[company_name] = []
        
        product_name = re.sub(r'[^a-zA-Z]+', ' ', result["product_name"]['S'])

        products[company_name].append(product_name)


    return products

def get_product_type(product_description_list):
    ## TODO ## 
    ## add fuzzy name matching

    important_descriptors = []

    for word in product_description_list:
        if word.lower() in PRODUCT_TYPE_SET:
            important_descriptors.append(word)
    
    return important_descriptors



def generate_synonyms(product_name):
    ## TODO ## 
    # some of the items dont contain any training data
    # create a smarter algorithm for capturing key words (used and inserting into examples)

    product_description_list = product_name.split()
    common_set = set()

    try:
        product_description_list.remove("&")
    except Exception as e:
        pass

    string_len = len(product_description_list)
    product_types = []

    synonyms = []

    if string_len/2 >= MATCH_WINDOW:
        synonyms.extend(list(itertools.combinations(product_description_list[:MATCH_WINDOW]+product_description_list[-MATCH_WINDOW:], MINIMUM_SIGNIFICANT_KEYWORDS)))
        # synonyms.append(tuple(product_description_list))
    elif string_len/2 < MATCH_WINDOW and string_len > 1: 
        synonyms.extend(list(itertools.combinations(product_description_list, string_len-1)))
    else:
        synonyms.append(tuple(product_description_list))
    
    unique_synonyms = []

    for synonym in synonyms:
        if synonym not in common_set:
            unique_synonyms.append(list(synonym))
            common_set.add(synonym)

    synonyms = unique_synonyms[:199]
    
    synonyms = [" ".join(synonym) for synonym in synonyms]
        
    return synonyms

def update_all(option="UPDATE"):

    company_products = get_brand_names()
    update_company_names(company_products)

    if option == "UPDATE":
        update_entities_with_database(company_products)
    elif option =="CREATE":
        create_entity_types_from_database(company_products)
    
    generate_intents_training_phrases(company_products)

def generate_intents_training_phrases(company_products=None):

    max_random_number = len(DEFAULT_SEARCH_PHRASES) - 1
    min_randon_number = 0

    if company_products == None:
        company_products = get_brand_names()
    
    for company_name in tqdm(company_products):
        for product in tqdm(company_products[company_name]):
            df.create_product_lookup_intent(brand_name=company_name, product_name=product)
            df.create_product_lookup_intent(brand_name=company_name, product_name=product, extra_text=DEFAULT_SEARCH_PHRASES[randint(min_randon_number,max_random_number)])
        
        time.sleep(300)


def update_company_names(company_products=None):

    if company_products == None:
        company_products = get_brand_names()

    entities = []
    for company_name in tqdm(company_products):
        entity = {
            'value': company_name,
            'synonyms': [company_name, company_name.lower()]
        }
        entities.append(entity)
    
    
    name = 'projects/newagent-hrmeto/agent/entityTypes/dd3c4230-d873-41d9-bd4c-d5e366cfb541'
    display_name = 'HairCompany'
    kind = "KIND_MAP"
    entities = entities
    
    df.update_entity(entity_path=name, entity_name=display_name, entities=entities)


def create_entity_types_from_database(company_products=None):

    if company_products == None:
        company_products = get_brand_names()
    
    for company_name in tqdm(company_products):
        entities = []
        for product in tqdm(company_products[company_name]):
            synos = generate_synonyms(product)
            print( "\n\n", company_name , product, synos, "\n\n")
            
            entity = {
                'value': product,
                'synonyms': synos
            }
            entities.append(entity)

        df.create_entity(brand_name=company_name.replace(" ", "").lower(),entities=entities)


def update_entities_with_database(company_products=None):

    if company_products == None:
        company_products = get_brand_names()
    
    for company_name in tqdm(company_products):
        company_entity_id = None
        # company_entity_id = get_entity_id(company_name.lower().replace(" ", ""))
       
        entities = []
        for product in tqdm(company_products[company_name]):
            synos = generate_synonyms(product)
            print( "\n\n", company_name , product, synos, "\n\n")

            entity = {
                'value': product,
                'synonyms': synos
            }
            entities.append(entity)
    
        entity_path = 'projects/newagent-hrmeto/agent/entityTypes/{}'.format(company_entity_id)
        entity_display_name = company_name.lower().replace(" ", "")+dialogflow_accessor.DEFAULT_NAME_APPENDAGE
        kind = dialogflow_accessor.DEFAULT_KIND

        df.update_entity(entity_path=entity_path, entity_name=entity_display_name, kind=kind, entities=entities)

df = dialogflow_accessor.DialogFlowClient("+19543984645")

while (True):


    options = """
    (Update) All EntityTypes
    (Add) Company Names
    (Create) Entity Types & Update Company Names
    (ALL) Update EntityTypes & Company Names
    (Intent) Creation
    (E) to (Exit)
    \n
    """
    string = input("{} \n >: ".format(options))

    if string.upper().strip() == 'UPDATE':
        update_entities_with_database()
        print("\nUpdating Entities...")

    elif string.upper().strip() == 'ADD':
        update_company_names()
        print("\nUpdating Company Names...")
    
    elif string.upper().strip() == 'CREATE':
        create_entity_types_from_database()
        print("\nCreate Company Entities...")

    elif string.upper().strip() == 'ALL':
        update_all()
        print("\nUpdating All ...")
    
    elif string.upper().strip() == 'INTENT':
        generate_intents_training_phrases()
        print("\nUpdateing Intents ...")

    elif string.upper().strip() == 'EXIT' or string.upper().strip() == 'E':
        break

    else:
        print("\nInvalid option")
