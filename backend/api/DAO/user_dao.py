from database_client import dynamo
from definitions import return_values
from util import data_util
from DAO import base_dao
from DAO import update_expression
import hashlib
import os
import hmac
import jwt
import datetime
import uuid

class User_DAO(base_dao.BaseDAO):
    def __init__(self,table_name):
        super().__init__(table_name)

    #Returns encoded password, given the plain one
    def encode_password(self,password, salt=None):
        if salt is None:
            salt = os.urandom(16)
        rounds = 100000
        hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, rounds)
        return {
            'hash': 'sha256',
            'salt': salt,
            'rounds': rounds,
            'hashed': hashed,
        }

    #[IMPLEMENTATION]
    # Create id for a item
    def create_item_id(self,item_param):
        return data_util.create_hash(item_param['name']) 

    #[IMPLEMENTATION]
    # Format item for writing operations 
    def format_item_for_writing(self,item_id,item_param):
        password_fields = self.encode_password(item_param['password'])
        item = {
            'id':{'S':item_id},
            'name':{'S':item_param['name']},
            'bought_assets':{'SS':item_param.get('bought_assets', [''])},
            'password':{'S':item_param['password']},
            'hash':{'B':password_fields['hash']},
            'salt':{'B':password_fields['salt']},
            'rounds':{'N':str(password_fields['rounds'])},
            'hashed':{'B':password_fields['hashed']}
            
        }
        return item

    #[IMPLEMENTATION] 
    #Format item from reading operations    
    def format_item_from_reading(self,read_item_data):
        
        print('DELETE DELETE DELETE DELETE DELETE DELETE ')
        print(read_item_data)
            
        if 'Item' in read_item_data:
            return  {
                        'name': read_item_data['Item']['name']['S'],
                        'password': read_item_data['Item']['password']['S'],
                        'bought_assets':read_item_data['Item']['bought_assets']['SS']
                    }
        return None

    #[IMPLEMENTATION] 
    #Create update expressions
    #Must return update expressions for update operations 
    def create_update_expression(self,item_param):
        expression = update_expression.UpdateExpression(
            "SET #n = :new_name, #p = :new_password,#b = :new_bought_assets",
            {"#n": "name", "#p": "password","#b":"bought_assets"},
            {
                ":new_name": {"S": item_param['name']},
                ":new_password": {"S": item_param['password']},
                ":new_bought_assets":{"SS":item_param.get('bought_assets', [''])}
            }
        )
        return expression
        
    #[IMPLEMENTATION] 
    #Validate item
    #Returns True or false
    def validate_item(self, item):
        field_names = ['name','password']
        if not all(field in item for field in field_names):
            return False
        if not all(isinstance(item[field], str) for field in field_names):
            return False
        return True

    #Process user login
    def user_login(self, username, password):
        id = data_util.create_hash(username)
        try:
            response = self.db_instance.client.get_item(
                    TableName = self.table_name,
                    Key = {'id': {'S': id}}
            )
            if 'Item' in response:
                user = response['Item']
                password_fields = {
                    'hash': user['hash']['B'],
                    'salt': user['salt']['B'],
                    'rounds': user['rounds']['N'],
                    'hashed': user['hashed']['B'],
                }
                hashed = self.encode_password(password, password_fields['salt'])
                if hashed['hashed'] == password_fields['hashed']:
                    return return_values.SUCCESS
                else:
                    return return_values.INVALID_INPUT_DATA
            else:
                return return_values.USER_NOT_FOUND
        except Exception as e:
            return str(e)

    def get_jwt_token(self,username, password):

        user_id = data_util.create_hash(username)

        db_record = self.read_user(user_id)

        actual = hashlib.pbkdf2_hmac(db_record['hash']['B'].decode('utf-8'), password.encode('utf-8'), db_record['salt']['B'], int(db_record['rounds']['N']))

        expected = db_record['hashed']['B']

        if hmac.compare_digest(actual, expected):
            now = datetime.datetime.utcnow()
            unique_id = str(uuid.uuid4())
            payload = {
                'sub': username,
                'iat': now,
                'nbf': now,
                'jti': unique_id,
            }
            return jwt.encode(payload, 'secret', algorithm='HS256')
        return return_values.INVALID_USER_OR_PASSWORD

    def decode_jwt_token(self,token):
        return jwt.decode(token, 'secret', algorithms=['HS256'])
    
