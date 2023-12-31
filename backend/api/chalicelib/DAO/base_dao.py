from chalicelib.database_client import dynamo
from chalicelib.definitions import return_values
import boto3


from chalicelib.util import data_util
from chalicelib.DAO import update_expression
import time

# Base class for DAO (Data Access Object). 
# Inherit from this class to implement 
# specific DynamoDB table access objects.

class BaseDAO:                 
    def __init__(self,table_name):
        self.table_name = table_name
        self.db_instance = dynamo.Dynamo_instance()
        
    #Create id for a item
    #Must be implemented by derivative class
    def create_item_id(self,item_param):
        #Example implementation: 
        #return data_util.create_hash(item_param['name']) 
        return None

    #Format item for writing operations 
    #Must be implemented by derivative class
    def format_item_for_writing(self,item_id,item_param):
        #Example: 
        #return {
        #    'id':{'S':item_id},
        #    'name':{'S':item_param['name']},
        #    'description':{'S':item_param['description']},
        #    'url':{'S':item_param['url']}
        #}
        return item_param

    #format item from reading operations    
    #Must be implemented by derivative class
    def format_item_from_reading(self,read_item_data):
        #Example: 
        #return  {
        #            'name': read_item_data['Item']['name']['S'],
        #            'description': read_item_data['Item']['description']['S'],
        #            'url': read_item_data['Item']['url']['S']
        #        }
        return read_item_data

    #Create update expressions
    #Must be implemented by derivative class
    #Must return update expressions for update operations 
    def create_update_expression(self,item_param):
        #Example:
        #expression = update_expression.UpdateExpression(
        #    "SET #n = :new_name, #d = :new_description,#u = :new_url",
        #    {"#n": "name", "#d": "description", "#u":"url"},
        #    {
        #        ":new_name": {"S": item_param['name']},
        #        ":new_description": {"S": item_param['description']},
        #        ":new_url": {"S": item_param['url']},
        #    }
        #)
        #return expression
        return None

    # Validate item
    #Must be implemented by derivative class
    #Must returns True or false
    def validate_item(self, item):
        #Example:
        #field_names = ['name','description','url']
        #if not all(field in item for field in field_names):
        #    return False
        #if not all(isinstance(item[field], str) for field in field_names):
        #    return False
        #return True
        return False

    # create DynamoDB table
    # return values:
    # TABLE_ALREADY_EXISTS
    # TIME_OUT
    # SUCCESS
    def create_table(self):
        if dynamo.check_table_existence(self.table_name):
            return return_values.TABLE_ALREADY_EXISTS
        table_params = {
            'TableName': self.table_name,
            'KeySchema': [
                {'AttributeName': 'id', 'KeyType': 'HASH'}
            ],
            'AttributeDefinitions': [
                {'AttributeName': 'id', 'AttributeType': 'S'}
            ],
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            } 
        }
        try:
            self.db_instance.client.create_table(**table_params)
        except Exception as e:
            return str(e)
        return dynamo.wait_table_creation(self.table_name)
    
    #Wait for an iten to exist with given values
    #Useful for checking update operation
    #returns True or False
    def wait_item_status(self, item_id):
        max_retries = 30 
        retries = 0
        print('\n Waiting for writing\n')
        while retries < max_retries:
            print('.', end=' ',flush=True)
            item = self.db_instance.client.get_item(TableName=self.table_name, Key={"id": {"S": item_id}})
            if 'Item' in item:
                mapped_values = self.format_item_from_reading(item)
                if self.validate_item(mapped_values):
                    return True 
            time.sleep(5)
            retries += 1
        return False


    #Create item 
    # return values:
    # TABLE_NOT_FOUND
    # TIME_OUT
    # SUCCESS
    def create_item(self,item_param):
        if not dynamo.check_table_existence(self.table_name):
            return return_values.TABLE_NOT_FOUND
        if not self.validate_item(item_param):
            return return_values.INVALID_INPUT_DATA
        id = self.create_item_id(item_param)
        if not self.read_item(id) == return_values.ITEM_NOT_FOUND:
            return return_values.ITEM_ALREADY_EXISTS
        item = self.format_item_for_writing(id,item_param)
        try:
            self.db_instance.client.put_item(
                TableName = self.table_name,
                Item = item
            )
        except Exception as e:
            error = str(e)
            return str(e)
        if self.wait_item_status(id):
            return id
        else:
            return return_values.ERROR + ": Writing not successfull"
        
    # Read an item 
    # return values:
    # The item data
    # TABLE_NOT_FOUND
    # INVALID_INPUT_DATA
    def read_item(self,item_id):
        if not dynamo.check_table_existence(self.table_name):
            return return_values.TABLE_NOT_FOUND
        if not item_id:
            return return_values.INVALID_INPUT_DATA
        try:
            response = self.db_instance.client.get_item(
                    TableName = self.table_name,
                    Key = {'id': {'S': item_id}}
            )
            if 'Item' in response:
                return self.format_item_from_reading(response['Item'])
            else:
                return return_values.ITEM_NOT_FOUND
        except Exception as e:
            return str(e)

    
    def read_all_items(self):
        if not dynamo.check_table_existence(self.table_name):
            return return_values.TABLE_NOT_FOUND
        try:
            response = self.db_instance.client.scan(
                    TableName=self.table_name
                    )
            if 'Items' in response:
                normalized_list = []
                for item in response['Items']:
                    normalized_item = self.format_item_from_reading(item)
                    normalized_list.append(normalized_item)
                return normalized_list
            return return_values.ITEM_NOT_FOUND
        except Exception as e:
            return str(e)

    # Update  item 
    # return values:
    # TABLE_NOT_FOUND
    # INVALID_INPUT_DATA
    # ITEM_NOT_FOUND
    # SUCCESS

    def update_item(self,item_id,item_param):
        if not dynamo.check_table_existence(self.table_name):
            return return_values.TABLE_NOT_FOUND
        
        if not self.validate_item(item_param) or not item_id:
            return return_values.INVALID_INPUT_DATA
        
        try:
            userInfo = self.read_item(item_id)
            notEmail =  item_param.get('email', True)
            notName = item_param.get('name', True)
            notPassword = item_param.get('password', True)
            notBalance = item_param.get('balance', True)
            if notName:
                item_param['name'] = userInfo['name']
            elif notEmail:
                if userInfo.get('email', False):
                    item_param['email'] = ''
                else:
                    item_param['email'] = userInfo['email']
            elif notPassword:
                item_param['password'] = userInfo['password']
            elif notBalance:
                item_param['balance'] = userInfo['balance']

            expression = self.create_update_expression(item_param)
            
            response = self.db_instance.client.update_item(
                TableName=self.table_name,
                Key={"id": {"S": item_id}},
                UpdateExpression=expression.expression,
                ExpressionAttributeNames=expression.attribute_names,
                ExpressionAttributeValues=expression.attribute_values,
            )
            

            if self.wait_item_status(item_id):
                return return_values.SUCCESS
            else:
                return return_values.ERROR + ": Update not successfull"
        except Exception as e:
            return return_values.ERROR +" : "+ str(e)


    # delete an item 
    # return values:
    # TABLE_NOT_FOUND
    # INVALID_INPUT_DATA
    # SUCCESS
    def delete_item(self,item_id):
        if not dynamo.check_table_existence(self.table_name):
            return return_values.TABLE_NOT_FOUND
        if not item_id:
            return return_values.INVALID_INPUT_DATA
        try:
            response = self.db_instance.client.delete_item(
                    TableName = self.table_name,
                    Key = {'id': {'S': item_id}}
            )
            return return_values.SUCCESS
        except Exception as e:
            return str(e)    
    
    #Serch items using keyword criteria
    #The string keyword will be searched on all attributes that are listed on attribute names.
    #Returns:
    #List of items
    #TABLE_NOT_FOUND
    #ITEM_NOT_FOUND
    def search_itens_by_keyword(self, keyword,attribute_names):
        filter_expression = str(' OR '.join([f'contains({attr}, :keyword)' for attr in attribute_names]))
        expression_attribute_values = {':keyword': {'S': keyword}}
        try:
            if not dynamo.check_table_existence(self.table_name):
                return return_values.TABLE_NOT_FOUND
            response = self.db_instance.client.scan(
                    TableName=self.table_name,
                    FilterExpression = filter_expression,
                    ExpressionAttributeValues=expression_attribute_values
                    )
            if 'Items' in response:
                return response
            return return_values.ITEM_NOT_FOUND
        except Exception as e:
            return str(e)    
    
    def delete_table(self):
        if dynamo.check_table_existence(self.table_name):
            self.db_instance.client.delete_table(TableName = self.table_name)
            return dynamo.wait_table_vanish(self.table_name)
        return return_values.TABLE_NOT_FOUND
