from database_client import dynamo
from definitions import return_values
from util import data_util
from DAO import base_dao
from DAO import update_expression


class Asset_DAO(base_dao.BaseDAO):
    def __init__(self,table_name):
        super().__init__(table_name)

    #[IMPLEMENTATION]
    # Create id for a item
    def create_item_id(self,item_param):
        return data_util.create_hash(item_param['title']) 

    #[IMPLEMENTATION]
    # Format item for writing operations 
    #Must be implemented by derivative class
    def format_item_for_writing(self,item_id,item_param):
        item = {
            'id':{'S':item_id},
            'title':{'S':item_param['title']},
            'description':{'S':item_param['description']},
            'web_address':{'S':item_param['web_address']}
        }
        return item

    #[IMPLEMENTATION] 
    #Format item from reading operations    
    def format_item_from_reading(self,read_item_data):
        return  {
                    'title': read_item_data['Item']['title']['S'],
                    'description': read_item_data['Item']['description']['S'],
                    'web_address': read_item_data['Item']['web_address']['S']
                }

    #[IMPLEMENTATION] 
    #Create update expressions
    #Must return update expressions for update operations 
    def create_update_expression(self,item_param):
        expression = update_expression.UpdateExpression(
            "SET #t = :new_title, #d = :new_description,#w = :new_web_address",
            {"#t": "title", "#d": "description", "#w":"web_address"},
            {
                ":new_title": {"S": item_param['title']},
                ":new_description": {"S": item_param['description']},
                ":new_web_address": {"S": item_param['web_address']},
            }
        )
        return expression
        
    #[IMPLEMENTATION] 
    #Validate item
    #Returns True or false
    def validate_item(self, item):
        field_names = ['title','description','web_address']
        if not all(field in item for field in field_names):
            return False
        if not all(isinstance(item[field], str) for field in field_names):
            return False
        return True
        
    