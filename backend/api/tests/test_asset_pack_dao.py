import pytest
from chalicelib.DAO import asset_pack_dao as dao
from chalicelib.util import data_util
from chalicelib.definitions import return_values,database_defs
import boto3
import time

class TestAsset_pack_DAO:
    _SLEEP = 10
    table_defs = database_defs.Table_Defs()
    table_names = table_defs.get_test_table_names()
    _asset_pack_table_name = table_names['asset_packet_table']
    _dao = None

    _skip_teardown = False

    @classmethod
    def _delete_table(cls):
        print('Entering _delete_table\n')
        cls._dao.delete_table()
        
    @classmethod
    def _get_table(cls):
        print('Entering _get_table\n')
        dynamodb = boto3.resource("dynamodb")
        response =  dynamodb.Table(cls._asset_pack_table_name)
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
        item =  cls._dao.read_item(item_id)
        return item

    @classmethod
    def _create_table_item(cls,name,description,url,store_media = []):
        table = cls._get_table()
        if table:
            asset_pack_param = {
                            'title': name,
                            'description': description,
                            'web_address': url,
                            'store_media':store_media
                        }
            
            asset_pack_id = cls._dao.create_item(asset_pack_param)
            return asset_pack_id
        return return_values.TABLE_NOT_FOUND

        
    #asset_pack_DAO must create a table that should be accessible by boto3
    def setup_class(self):
        print('\n[[Entering setup_class]]\n')
        print(self._asset_pack_table_name)
        self._dao = dao.Asset_pack_DAO(self._asset_pack_table_name)
        ret_value = self._dao.create_table()
        print('create_asset_pack_table: '+ ret_value)
        table_status = self._get_table_status() 
        assert table_status == "ACTIVE",f'Error: asset_pack table is suposed to be active'
    
        
    #asset_pack_DAO must create item on asset_pack table
    def test_create_asset_pack(self):
        print('\n[[Entering test_create_asset_pack]]\n')
        store_media_param = [
                                {'web_address': 'http://www.archive.com/24376/thumb1.png','type':'thumbnail'},
                                {'web_address': 'http://www.archive.com/24376/thumb2.png','type':'thumbnail'}
                            ]
        asset_pack_param = {'title': 'Medieval Tileset',
                      'description': 'A packet containing medieval themed tilesets for 2D RPG Games',
                      'web_address': 'http://www.archive.com/63482/medievaltiles.zip',
                      'store_media': store_media_param }
        
        id = self._dao.create_item(asset_pack_param)
        print('expected item id as response. Received ' + id)
        
        response = self._get_table_item(id)
        print(response)
        
        assert response["title"] == asset_pack_param["title"],f'Error testing created asset_pack. name diverges'
        assert response["description"] == asset_pack_param["description"],f'Error testing created asset_pack. description diverges'
        assert response["web_address"] == asset_pack_param["web_address"],f'Error testing created asset_pack. url diverges'
        assert response["store_media"] == asset_pack_param["store_media"],f'Error testing created asset_pack. store media diverges'

    #It must be possible to omit store media durint asset pack creation
    def test_create_asset_pack_without_store_media(self):
        print('\n[[Entering test_create_asset_pack_without_store_media]]\n')
        asset_pack_param = {'title': 'Epic music',
                      'description': 'A packet 7 mp3 tracks of symphonic epic themes',
                      'web_address': 'http://www.archive.com/6348dfsj2/Ephic_suit_music.zip'
                        }
        
        id = self._dao.create_item(asset_pack_param)
        print('expected item id as response. Received ' + id)

        response = self._get_table_item(id)
        print(response)
        
        assert response["title"] == asset_pack_param["title"],f'Error testing created asset_pack. name diverges'
        assert response["description"] == asset_pack_param["description"],f'Error testing created asset_pack. description diverges'
        assert response["web_address"] == asset_pack_param["web_address"],f'Error testing created asset_pack. url diverges'
        assert response["store_media"] == [],f'Error testing created asset_pack. store media diverges'



    #asset_pack_DAO must read an existing asset_pack
    def test_read_asset_pack(self):
        print('\n[[Entering test_read_asset_pack]]\n')
        table = self._get_table()
        if table:
            store_media_param = [
                                {'web_address': 'http://www.archive.com/24376/thumb1.png','type':'thumbnail'},
                                {'web_address': 'http://www.archive.com/24376/thumb2.png','type':'thumbnail'}
                            ]
        
            asset_pack_param = {
                'title':'Spaceship sprites',
                'description':'2D top down spaceship sprites',
                'web_address':'http://www.archive.com/68758sfs850/2dSpaceships.zip',
                'store_media': store_media_param
            }
            asset_pack_id = self._create_table_item(asset_pack_param['title'],
                                asset_pack_param['description'],
                                asset_pack_param['web_address'],
                                asset_pack_param['store_media'])

            assert asset_pack_id != return_values.TABLE_NOT_FOUND,f'Error creating item before deletion'
            
            response = self._dao.read_item(asset_pack_id)
            
            assert response == {
                'id':asset_pack_id,
                'title':asset_pack_param['title'],
                'description':asset_pack_param['description'],
                'web_address':asset_pack_param['web_address'],
                'store_media':store_media_param
            },f'Error reading asset_pack. Incorrect response'
        else:
            print("Test skipped (asset_pack Table not found)\n")    
    
    #asset_pack_DAO must update an existing asset_pack
    def test_update_asset_pack(self):
        print('\n[[Entering test_update_asset_pack]]\n')
        table = self._get_table()
        if table:
            
            store_media_param = [
                                {'web_address': 'http://www.archive.com/24376/thumb1.png','type':'thumbnail'},
                                {'web_address': 'http://www.archive.com/24376/thumb2.png','type':'thumbnail'}
                            ]
        
            asset_pack_id = self._create_table_item('Spaceship sprites',
                                '2D top down spaceship sprites',
                                'http://www.archive.com/68758sfs850/2dSpaceships.zip',
                                 store_media_param)
                    
            assert asset_pack_id != return_values.TABLE_NOT_FOUND,f'Error creating item before deletion'
            
            updated_store_media_param = [
                                {'web_address': 'http://www.archive.com/update24376/updated_thumb1.png','type':'thumbnail'},
                                {'web_address': 'http://www.archive.com/update24376/updated_thumb2.png','type':'thumbnail'}
                            ]

            updated_item_param = {
                'title':'2D city textures',
                'description':'Set of realistic textures for urban locations',
                'web_address':'http://www.archive.com/68758850/urban_textures.zip',
                'store_media': updated_store_media_param
            }
            
            result = self._dao.update_item(asset_pack_id,updated_item_param)

            assert result == return_values.SUCCESS,f'Error testing asset_pack update. Incorrect response'
            
            response = self._get_table_item(asset_pack_id)
            assert response['title'] == updated_item_param['title'], f'asset_pack name not properly updated '
            assert response['description'] == updated_item_param['description'], f'asset_pack description not properly updated'
            assert response['web_address'] == updated_item_param['web_address'], f'asset_pack url not properly updated'
            assert response['store_media'] == updated_item_param['store_media'], f'asset_pack store_media not properly updated'

        else:
            print("Test skipped (asset_pack Table not found)\n")

    #asset_pack_DAO must delete an existing asset_pack
    def test_delete_asset_pack(self):
        print('\n[[Entering test_delete_asset_pack]]\n')
        table = self._get_table()
        if table:
            asset_pack_id = self._create_table_item('Spaceship sprites',
                                '2D top down spaceship sprites',
                                'http://www.archive.com/68758sfs850/2dSpaceships.zip',
                                )
            assert asset_pack_id != return_values.TABLE_NOT_FOUND,f'Error: item not created (TABLE NOT FOUND)'
            result = self._dao.delete_item(asset_pack_id)
            assert result == return_values.SUCCESS,f'Error testing delete asset_pack. Incorrect response'
            response = table.get_item(Key={'id':asset_pack_id})
            assert 'Item' not in response,f'Error testing delete asset_pack. Bad response'
        else:
            printf("Test skipped (asset_pack table not found)\n")

    #It must be possible to search asset_packs by keyword
    def test_search_asset_packs_by_keyword(self):
        print('\n[[Entering test_search_asset_packs_by_keyword]]\n')
        table = self._get_table()
        if table:
            asset_pack_id1 = self._create_table_item('name 1',
                                'description 1',
                                'url 1')
            assert asset_pack_id1 != return_values.TABLE_NOT_FOUND,f'Error creating item before deletion'
            asset_pack_id2 = self._create_table_item('name 2',
                                'description 2',
                                'url 2')
            assert asset_pack_id2 != return_values.TABLE_NOT_FOUND,f'Error creating item before deletion'
            asset_pack_id3 = self._create_table_item('name 3',
                                'description 3',
                                'url 3')
            assert asset_pack_id3 != return_values.TABLE_NOT_FOUND,f'Error creating item before deletion'
            
            test_result1 = self._dao.search_itens_by_keyword("name 1",{'title','description','web_address'})
            print(test_result1)
            print('\n')
            assert test_result1['Items'][0]['id']['S']==asset_pack_id1

            test_result2 = self._dao.search_itens_by_keyword("description 2",{'title','description','web_address'})
            print(test_result2)
            print('\n')
            assert test_result2['Items'][0]['id']['S']==asset_pack_id2
            
            test_result3 = self._dao.search_itens_by_keyword("url 3",{'title','description','web_address'})
            print(test_result3)
            print('\n')
            assert test_result3['Items'][0]['id']['S']==asset_pack_id3

            test_result4 = self._dao.search_itens_by_keyword("url",{'title','description','web_address'})
            print(test_result4)
            print('\n')
            assert test_result4['Count']==3

        else:
            printf("Test skipped (asset_pack table not found)\n")

    def teardown_class(self):
        print('\n[[Entering teardown_class]]\n')
        if self._skip_teardown:
            print('\n Teardown skipped \n')
            return
        self._delete_table()

