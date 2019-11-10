import boto3 # aws sdk
from elasticsearch import Elasticsearch # elasticsearch client sdk
S3 has the ability to trigger an AWS Lambda function whenever a new object is added or deleted, passing to the function’s environment the information, such as the name of the object, bucket in which to object is stored, etc.
def lambda_handler(context, event): # signature for the lambda function
# lets initialize the AWS Glue client and the elasticsearh client
glue_client = boto3.resource('glue') # we will use glue to get schema information about the data
es_client = Elasticsearch([{
'host': ELASTICSEARCH_HOST,
'port': ELASTICSEARCH_PORT
}])
That Lambda function could then go on and add additional data about the object that was created, such as who created it, how long should the object remain in storage, which team the object is available to, the schema of the objects, (since we now have that information available, thanks to AWS Glue) and what is the size of that data.
glue_response = glue_client.get_table(
CatalogId=CATALOG_ID, # the id of the data catalog where the data resides
DatabaseName=DATABASE_NAME, # the name of the database in which the table resides
Name=NAME # the name of the table for which to retrieve the definition
) # the response of this command is a dict
schema_data = glue_response['Table']['StorageDescriptor']
In short, the function could provide metadata about the object that was created. 
# now we have to generate a metadata dict to store in elastic search
metadata_dict = {
'created': datetime.datetime.now(),
'owner': 'owner',
'bucket': bucket,
'filename': filename,
'availableTo': ['Advanced Analytics', 'Machine Learning'],
# additional data can be added as needed
'schema': schema_data
}
