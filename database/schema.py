string = "S"
number = "N"
binary = "B"

product_schema = {

    key_var = "product_name"
    
    attributes = {
        "ingredients": string,
        "product_image_url": string,
        "product_url": string
    }
    
}

user_schema = {
    
    key_var = "user_phone"

    attributes = {
        "email" : string,
        "name" : string, 
        "porosity" : string,
        "density" : string,
        "curl_type" : string,
        "send_promotions_bool" : string,
        "location" : string
    }
}

user_product_searches = {
    
    key_var = "user_phone"

    attributes = {
        "phone_number" : string,
        "product_name" : string,
        "product_brand" : string
    }
}