from database_accessor import database
import db_schemas

schemas = {
"product" : db_schemas.product_schema,
"user" :  db_schemas.user_schema,
"searches" :  db_schemas.user_product_searches,
"messages" : db_schemas.user_messages
}

while (True):

    options = """
    (Create) Table
    (Clear) Table
    (E) to (Exit)
    \n
    """
    string = input("{} \n What would you like to do: ".format(options))

    if string.upper().strip() == 'CREATE':
        tablename = input("Enter TableName: ")
        if tablename in schemas:
            schema = schemas[tablename]

            database.create_table(
                tablename=tablename,
                key_var=schema["key_var"],
                range_var=schema["range_var"],
                attributes=schema["attributes"]
            )
        
            print("table created successfully")

        else:
            print("Not support at this time")
            continue
    
    if string.upper().strip() == 'CLEAR':
        tablename = input("Enter TableName: ")
        if tablename in schemas:
            schema = schemas[tablename]
            try:
                database.clear_table(tablename, schema["key_var"], schema["range_var"])
                print("table cleared successfully")
            except Exception as e:
                print("couldn't clear table =%s", e)
                continue
    

    if string.upper().strip() == 'EXIT' or string.upper().strip()== "E":
        break



    