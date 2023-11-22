from chalicelib.database_client import dynamo
from chalicelib.definitions import return_values
from chalicelib.util import data_util
from chalicelib.DAO import base_dao
from chalicelib.DAO import update_expression


class Asset_pack_DAO(base_dao.BaseDAO):
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
        formated_store_media = []
        store_media = item_param['store_media'] 
        if store_media:
            for media in store_media:
                formated_media = {'M':{
                    'web_address':{'S':media['web_address']},
                    'type':{'S':media['type']}
                    }}
                formated_store_media.append(formated_media)
        
        item = {
            'id':{'S':item_id},
            'title':{'S':item_param['title']},
            'description':{'S':item_param['description']},
            'web_address':{'S':item_param['web_address']},
            'store_media':{'L':formated_store_media},

        }
        return item

    #[IMPLEMENTATION] 
    #Format item from reading operations    
    def format_item_from_reading(self,read_item_data):
        
        store_media = []

        if 'Item' in read_item_data:
            item = read_item_data['Item']
        else:
            item = read_item_data
        
        if 'store_media' in read_item_data:
            read_store_media = item['store_media']['L']     
            if read_store_media:
                for media in read_store_media:
                    store_media.append({
                    'web_address':media['M']['web_address']['S'],
                    'type':media['M']['type']['S']
                    }) 

        return  {
            'title': item['title']['S'],
            'description': item['description']['S'],
            'web_address': item['web_address']['S'],
            'id': item['id']['S'],
            'store_media':store_media
        }

    #[IMPLEMENTATION] 
    #Create update expressions
    #Must return update expressions for update operations 
    def create_update_expression(self,item_param):
        formated_store_media = []        
        store_media = item_param.get('store_media',[])
        for media in store_media:
            formated_store_media.append({"M":{
                'web_address':{"S":media['web_address']},
                'type':{"S":media['type']}
            }}) 

        expression = update_expression.UpdateExpression(
            "SET #t = :new_title, #d = :new_description,#w = :new_web_address,#stm = :new_store_media",
            {"#t": "title", "#d": "description", "#w":"web_address","#stm":"store_media"},
            {
                ":new_title": {"S": item_param['title']},
                ":new_description": {"S": item_param['description']},
                ":new_web_address": {"S": item_param['web_address']},
                ":new_store_media":{"L":formated_store_media}
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
        
    