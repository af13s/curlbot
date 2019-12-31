
import os
import boto3

AWS_ACCESS_KEY_ID = "AKIAIB3ZH7H5B4FNUM2Q"
AWS_SECRET_ACCESS_KEY = "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"
REGION_NAME='us-west-1'

READ_CAPACITY_DEFAULT = 5
WRITE_CAPACITY_DEFAULT = 5

class database:

    @staticmethod
    def admin_session():
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

        return session

    @staticmethod
    def dynambo_admin_session():
        session = database.admin_session()
        dynamodb = session.resource('dynamodb', region_name=REGION_NAME)

        return dynamodb
    
    @staticmethod
    def dynambo_admin_client():
        session = database.admin_session()
        dynamodb = boto3.client('dynamodb', region_name=REGION_NAME)

        return dynamodb

    @staticmethod
    def create_table(tablename, key_var, range_var, attributes):

        dynamodb = database.dynambo_admin_session()

        if range_var is not None:
            keySchema = [
                {
                    'AttributeName': key_var,
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': range_var,
                    'KeyType': 'RANGE'
                },
            ]
        else:
            keySchema = [{'AttributeName': key_var,   'KeyType': 'HASH'}]

        attributeDefinitions = []
        for key, value in attributes.items():
            attribute = {}
            attribute["AttributeName"] = key
            attribute["AttributeType"] = value
            attributeDefinitions.append(attribute)
        
        print(keySchema, attributeDefinitions)
        
        provisionedThroughput={
            'ReadCapacityUnits': READ_CAPACITY_DEFAULT,
            'WriteCapacityUnits': WRITE_CAPACITY_DEFAULT,
        }

        table = dynamodb.create_table(
            TableName=tablename,
            KeySchema=keySchema,
            AttributeDefinitions=attributeDefinitions,
            ProvisionedThroughput=provisionedThroughput
        )

        print(table)

        table.meta.client.get_waiter('table_exists').wait(TableName=tablename)

    @staticmethod
    def clear_table(tablename, key_var, range_var):
        dynamodb = database.dynambo_admin_session()
        table = dynamodb.Table(tablename)
        result = table.scan()

	    # result = json.loads(result["Items"])
        with table.batch_writer() as batch:
            for obj in result["Items"]:
                batch.delete_item(Key={
                    key_var: obj["product_name"],
                    range_var: obj["brand_name"]
                })

        print(tablename, "cleared")
    
    @staticmethod
    def add_table_entry(tablename, item):
        dynamodb = database.dynambo_admin_session()
        table = dynamodb.Table(tablename)
        table.put_item(Item=item)

    @staticmethod
    def add_table_batch(tablename, items):
        dynamodb = database.dynambo_admin_session()
        table = dynamodb.Table(tablename)
        with table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)

# add config to environment variables

    