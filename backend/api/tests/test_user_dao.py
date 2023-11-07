import pytest
from DAO import user_dao as dao
from util import data_util
from definitions import return_values
import boto3
import time

class TestUserDAO:
    _SLEEP = 10
    _user_table_name = "TestUserTable"
    _dao = None

    @classmethod
    def _delete_table(cls):
        print('Entering _delete_table\n')
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(cls._user_table_name)
        if table:
            table.delete()
            print("Table deleted\n")
            time.sleep(cls._SLEEP)
        print('Table was not deleted (Not found)\n')

    @classmethod
    def _get_table(cls):
        print('Entering _get_table\n')
        dynamodb = boto3.resource("dynamodb")
        response =  dynamodb.Table(cls._user_table_name)
        return response

    @classmethod    
    def _get_table_status(cls):
        print('Entering _get_table_status\n')
        table = cls._get_table()
        if table:
            return table.table_status
        return return_values.TABLE_NOT_FOUND

    @classmethod
    def _create_table_item(cls,name,password,bought_assets):
        table = cls._get_table()
        if table:
            user_param = {
                            'name': name,
                            'password': password,
                            'bought_assets': bought_assets
                        }
            
            user_id = cls._dao.create_item(user_param)
            
            return user_id
        return return_values.TABLE_NOT_FOUND


    @classmethod
    def _get_table_item(cls,item_id):
        print('Entering _get_table_item\n')
        item = cls._dao.read_item(item_id)
        return item
        
    
    #User_DAO must create a table that should be accessible by boto3
    def setup_class(self):
        print('\n[[Entering setup_class]]\n')
        self._dao = dao.User_DAO(self._user_table_name)
        ret_value = self._dao.create_table()
        print('create_user_table: '+ ret_value)
        table_status = self._get_table_status() 
        assert table_status == "ACTIVE",f'Error: User table is suposed to be active'
    
        
    #User_DAO must create item on user table
    def test_create_user(self):
        print('\n[[Entering test_create_user]]\n')
        
        user_param = {
                'name':'Dino da Silva Sauro',
                'password':'123456',
                'bought_assets':['']
            }
        user_id = self._dao.create_item(user_param)
        
        assert user_id != return_values.TABLE_NOT_FOUND,f'Error creating user (table not found)'
        response = self._get_table_item(user_id)
        print(response)
        assert response["name"] == user_param["name"],f'Error testing created user. name diverges'
        assert response["password"] == user_param["password"],f'Error testing created user. password diverges'
    
    #User_DAO must read an existing user
    def test_read_user(self):
        print('\n[[Entering test_read_user]]\n')
        table = self._get_table()
        if table:
            user_param = {
                'name':'Fran da Silva Sauro',
                'password':'mypass',
                'bought_assets':['']
            }
            user_id = self._create_table_item(
                user_param['name'],
                user_param['password'],
                user_param['bought_assets']
            )
            assert user_id != return_values.TABLE_NOT_FOUND,f'Error creating user (table not found)'
        
            response = self._dao.read_item(user_id)
            
            assert response == {
                'name':user_param['name'],
                'password':user_param['password'],
                'bought_assets':user_param['bought_assets']
            },f'Error reading user. Incorrect response'
        else:
            print("Test skipped (User Table not found)\n")    

    #User_DAO must update an existing user
    def test_update_user(self):
        print('\n[[Entering test_update_user]]\n')
        table = self._get_table()
        if table:
            user_param = {
                'name':'Mônica Invertebrada',
                'password': 'blue',
                'bought_assets':['']
            }
            user_id = self._create_table_item(user_param['name'],
                                        user_param['password'],
                                        user_param['bought_assets'])
            assert user_id != return_values.TABLE_NOT_FOUND,f'Error creating user (table not found)'
        
            updated_item_param = {
                'name':'Roy Hess',
                'password':'Brown',
                'bought_assets':['']
            }

            result = self._dao.update_item(user_id,updated_item_param)
            assert result == return_values.SUCCESS,f'Error testing user update. Incorrect response'
            
            response = self._get_table_item(user_id)
            assert response['name'] == updated_item_param['name'], f'user name not properly updated '
            assert response['password'] == updated_item_param['password'], f'user password not properly updated'
            assert response['bought_assets'] == updated_item_param['bought_assets'], f'user bought assets not properly updated'
            
        else:
            print("Test skipped (user Table not found)\n")

    #User_DAO must delete an existing user
    def test_delete_user(self):
        print('\n[[Entering test_delete_user]]\n')
        table = self._get_table()
        if table:
            user_id = self._create_table_item('Sr. Richfield',
                                        'TheBo$$',
                                        [''])
            assert user_id != return_values.TABLE_NOT_FOUND,f'Error creating user (table not found)'

            result = self._dao.delete_item(user_id)

            assert result == return_values.SUCCESS,f'Error testing delete user. Incorrect response'
            response = table.get_item(Key={'id':user_id})
            assert 'Item' not in response,f'Error testing delete user. Bad response'
        else:
            printf("Test skipped (User table not found)\n")

    def teardown_class(self):
        print('\n[[Entering teardown_class]]\n')
        self._delete_table()

