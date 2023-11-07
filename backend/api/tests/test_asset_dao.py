import pytest
from DAO import asset_dao as dao
from util import data_util
from definitions import return_values
import boto3
import time

class TestAssetDAO:
    _SLEEP = 10
    _asset_table_name = "TestAssetTable"
    _dao = None

    @classmethod
    def _delete_table(cls):
        print('Entering _delete_table\n')
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(cls._asset_table_name)
        if table:
            table.delete()
            print("Table deleted\n")
            time.sleep(cls._SLEEP)
        print('Table was not deleted (Not found)\n')

    @classmethod
    def _get_table(cls):
        print('Entering _get_table\n')
        dynamodb = boto3.resource("dynamodb")
        response =  dynamodb.Table(cls._asset_table_name)
        return response

    @classmethod    
    def _get_table_status(cls):
        print('Entering _get_table_status\n')
        table = cls._get_table()
        if table:
            return table.table_status
        return return_values.TABLE_NOT_FOUND

    @classmethod
    def _get_table_item(cls,item_id):
        print('Entering _get_table_item\n')
        table = cls._get_table()
        if table:
            item =  table.get_item(
                Key={
                    'id':item_id
                }
            )
            assert 'Item' in item,f'Error Item not found'
            return item['Item']
        return return_values.TABLE_NOT_FOUND

    @classmethod
    def _create_table_item(cls,name,description,url):
        table = cls._get_table()
        if table:
            asset_param = {
                            'title': name,
                            'description': description,
                            'web_address': url
                        }
            
            asset_id = cls._dao.create_item(asset_param)
            return asset_id
        return return_values.TABLE_NOT_FOUND

        
    #asset_DAO must create a table that should be accessible by boto3
    def setup_class(self):
        self._dao = dao.Asset_DAO(self._asset_table_name)
        print('\n[[Entering setup_class]]\n')
        ret_value = self._dao.create_table()
        print('create_asset_table: '+ ret_value)
        table_status = self._get_table_status() 
        assert table_status == "ACTIVE",f'Error: asset table is suposed to be active'
    
        
    #asset_DAO must create item on asset table
    def test_create_asset(self):
        print('\n[[Entering test_create_asset]]\n')
        asset_param = {'title': 'Medieval Tileset',
                      'description': 'A packet containing medieval themed tilesets for 2D RPG Games',
                      'web_address': 'http://www.archive.com/63482/medievaltiles.zip'}
        id = self._dao.create_item(asset_param)
        print('expected item id as response. Received ' + id)
        time.sleep(self._SLEEP)
        response = self._get_table_item(id)
        print(response)
        assert response["title"] == asset_param["title"],f'Error testing created asset. name diverges'
        assert response["description"] == asset_param["description"],f'Error testing created asset. description diverges'
        assert response["web_address"] == asset_param["web_address"],f'Error testing created asset. url diverges'
    
    #asset_DAO must read an existing asset
    def test_read_asset(self):
        print('\n[[Entering test_read_asset]]\n')
        table = self._get_table()
        if table:
            asset_param = {
                'title':'Spaceship sprites',
                'description':'2D top down spaceship sprites',
                'web_address':'http://www.archive.com/68758sfs850/2dSpaceships.zip'
            }
            asset_id = self._create_table_item(asset_param['title'],
                                asset_param['description'],
                                asset_param['web_address'])
            assert asset_id != return_values.TABLE_NOT_FOUND,f'Error creating item before deletion'
            
            response = self._dao.read_item(asset_id)
            
            assert response == {
                'title':asset_param['title'],
                'description':asset_param['description'],
                'web_address':asset_param['web_address']
            },f'Error reading asset. Incorrect response'
        else:
            print("Test skipped (asset Table not found)\n")    

    #asset_DAO must update an existing asset
    def test_update_asset(self):
        print('\n[[Entering test_update_asset]]\n')
        table = self._get_table()
        if table:
            asset_id = self._create_table_item('Spaceship sprites',
                                '2D top down spaceship sprites',
                                'http://www.archive.com/68758sfs850/2dSpaceships.zip')
            assert asset_id != return_values.TABLE_NOT_FOUND,f'Error creating item before deletion'
            updated_item_param = {
                'title':'2D city textures',
                'description':'Set of realistic textures for urban locations',
                'web_address':'http://www.archive.com/68758850/urban_textures.zip'
            }
            result = self._dao.update_item(asset_id,updated_item_param)
            print(result)
            assert result == return_values.SUCCESS,f'Error testing asset update. Incorrect response'
            response = table.get_item(Key={'id': asset_id})
            updated_item = response.get('Item', {})
            assert updated_item['title'] == updated_item_param['title'], f'asset name not properly updated '
            assert updated_item['description'] == updated_item_param['description'], f'asset description not properly updated'
            assert updated_item['web_address'] == updated_item_param['web_address'], f'asset url not properly updated'
            
        else:
            print("Test skipped (asset Table not found)\n")

    #asset_DAO must delete an existing asset
    def test_delete_asset(self):
        print('\n[[Entering test_delete_asset]]\n')
        table = self._get_table()
        if table:
            asset_id = self._create_table_item('Spaceship sprites',
                                '2D top down spaceship sprites',
                                'http://www.archive.com/68758sfs850/2dSpaceships.zip')
            assert asset_id != return_values.TABLE_NOT_FOUND,f'Error: item not created (TABLE NOT FOUND)'
            result = self._dao.delete_item(asset_id)
            assert result == return_values.SUCCESS,f'Error testing delete asset. Incorrect response'
            response = table.get_item(Key={'id':asset_id})
            assert 'Item' not in response,f'Error testing delete asset. Bad response'
        else:
            printf("Test skipped (asset table not found)\n")

    #It must be possible to search assets by keyword
    def test_search_assets_by_keyword(self):
        print('\n[[Entering test_search_assets_by_keyword]]\n')
        table = self._get_table()
        if table:
            asset_id1 = self._create_table_item('name 1',
                                'description 1',
                                'url 1')
            assert asset_id1 != return_values.TABLE_NOT_FOUND,f'Error creating item before deletion'
            asset_id2 = self._create_table_item('name 2',
                                'description 2',
                                'url 2')
            assert asset_id2 != return_values.TABLE_NOT_FOUND,f'Error creating item before deletion'
            asset_id3 = self._create_table_item('name 3',
                                'description 3',
                                'url 3')
            assert asset_id3 != return_values.TABLE_NOT_FOUND,f'Error creating item before deletion'
            
            test_result1 = self._dao.search_itens_by_keyword("name 1",{'title','description','web_address'})
            print(test_result1)
            print('\n')
            assert test_result1['Items'][0]['id']['S']==asset_id1

            test_result2 = self._dao.search_itens_by_keyword("description 2",{'title','description','web_address'})
            print(test_result2)
            print('\n')
            assert test_result2['Items'][0]['id']['S']==asset_id2
            
            test_result3 = self._dao.search_itens_by_keyword("url 3",{'title','description','web_address'})
            print(test_result3)
            print('\n')
            assert test_result3['Items'][0]['id']['S']==asset_id3

            test_result4 = self._dao.search_itens_by_keyword("url",{'title','description','web_address'})
            print(test_result4)
            print('\n')
            assert test_result4['Count']==3

        else:
            printf("Test skipped (asset table not found)\n")




    def teardown_class(self):
        print('\n[[Entering teardown_class]]\n')
        self._delete_table()

