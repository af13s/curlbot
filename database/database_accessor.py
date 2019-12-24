
import boto3

AWS_ACCESS_KEY_ID =os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
REGION_NAME='us-east-1'

READ_CAPACITY_DEFAULT = 5
WRITE_CAPACITY_DEFAULT = 5

class database:

    @staticmethod
    def admin_session(self):
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

        return session

    @staticmethod
    def dynambo_admin_session():
        session = self.admin_session()
        dynamodb = session.resource('dynamodb', region_name=REGION_NAME)

        return dynamodb

    @staticmethod
    def create_table(self,tablename, key_var, range_var, kwargs):

        dynamodb = self.dynambo_admin_session()
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

        attributeDefinitions = []
        for key, value in kwargs.items():
            attribute = {}
            attribute["AttributeName"] = key
            attribute["AttributeType"] = value
            AttributeDefinitions.append(attribute)
        
        provisionedThroughput={
            'ReadCapacityUnits': READ_CAPACITY_DEFAULT,
            'WriteCapacityUnits': WRITE_CAPACITY_DEFAULT,
        }

        table = dynamodb.create_table(
            TableName=tablename,
            KeySchema=keySchema,
            AttributeDefinitions=attributeDefinitions
            ProvisionedThroughput=provisionedThroughput
        )

        table.meta.client.get_waiter('table_exists').wait(TableName=tablename)

    @staticmethod
    def clear_table(tablename, key_var, range_var):
        dynamodb = self.dynambo_admin_session()
        table = dynamodb.Table(tablename)
	    result = table.scan()

	    # result = json.loads(result["Items"])

	    for obj in result["Items"]:
		    deleteEvent(obj[key_var],obj[range_var])

	    print("Events Deleted")
    
    @staticmethod
    def add_table_entry(tablename, item):
        dynamodb = self.dynambo_admin_session()
        table = dynamodb.Table(tablename)
        table.put_item={
            Item=item
        }

    @staticmethod
    def add_table_batch(tablename, items):
        dynamodb = self.dynambo_admin_session()
        table = dynamodb.Table(tablename)
        with table.batch_writer() as batch:
            for item in items:
                batch.put_item({
                    Item=item
                })

# add config to environment variables

    