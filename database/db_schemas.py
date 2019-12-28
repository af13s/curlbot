string = "S"
number = "N"
binary = "B"

product_schema = {

    "key_var" : "product_name",
    "range_var" : "brand_name",
    
    "attributes" : {
        "product_name": string,
        "brand_name": string,
        # "ingredients": string,
        # "image_url": string,
        # "product_url": string
    }
}

user_messages = {

     "key_var" : "user_phone",
    "range_var" : "datetime",

    "attributes" : {
        "user_phone": string,
        "datetime": string,
        # "message": string,
        # "datetime_epoch": number,
    }
}

user_schema = {
    
    "key_var" : "user_phone",
    "range_var" : None,

    "attributes" : {
        "user_phone": string,
        # datetime: string,
        # "email" : string,
        # "name" : string, 
        # "porosity" : string,
        # "density" : string,
        # "curl_type" : string,
        # "send_promotions_bool" : string,
        # "location" : string
    }
}

user_product_searches = {
    
    "key_var" : "user_phone",
    "range_var" : "datetime",

    "attributes" : {
        "user_phone": string,
        "datetime": string
        # "product_name" : string,
        # "brand_name" : string
        # datetime_epoch: number
    }
}