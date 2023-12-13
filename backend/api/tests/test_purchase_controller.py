import pytest
from chalicelib.DAO import asset_pack_dao
from chalicelib.DAO import user_dao 
from chalicelib.controllers import purchase_controller
from chalicelib.util import data_util
from chalicelib.definitions import return_values
from chalicelib.definitions import database_defs
import boto3
import time

class Test_Purchase_Controller:
    _asset_pack_dao = None
    _user_dao = None

    table_defs = database_defs.Table_Defs()
    table_names = table_defs.get_test_table_names()
    
    _user_table_name = table_names['user_table']
    _asset_pack_table_name = table_names['asset_packet_table']

    _skip_teardown = False

    def setup_class(self):
        print('\n[[Entering setup_class]]\n')
        self._asset_pack_dao = asset_pack_dao.Asset_pack_DAO(self._asset_pack_table_name)
        self._user_dao = user_dao.User_DAO(self._user_table_name)
        
        self._purchase = purchase_controller.Purchase_Controller()
        self._purchase.set_table_names(self._user_table_name,self._asset_pack_table_name)        
        
        assert self._user_dao.create_table() == return_values.SUCCESS,f'Error creating user table'
        assert self._asset_pack_dao.create_table() == return_values.SUCCESS,f'Error creating asset pack table'
    
    #it must to be possible to purchase an asset pack
    def test_purchase_asset_pack(self):
        print('\n[[Entering test_purchase_asset_pack]]\n')
        
        asset_pack_param = {'title': "FPS FX",
                        'description': "Realistic sound effects intended for a contemporary war themed first person shooter",
                        'web_address': "http://www.archive.com/3726746273/Modern_war_Sound_FX.zip",
                        'cost':'5'}
                        
        
        user_param = {'name':'Dino da Silva Sauro',
                      'password':"password",
                      'balance':'10'
                      }

        user_id = self._user_dao.create_item(user_param)
        asset_pack_id = self._asset_pack_dao.create_item(asset_pack_param)

        result = self._purchase.purchase_asset_pack(user_id,asset_pack_id)
        assert result == return_values.SUCCESS,f'Error purchasing item'
        
        ret_user = self._user_dao.read_item(user_id)
        assert asset_pack_id in ret_user['purchased_asset_packs'],f'Error updating purchased list after purchasing asset pack'        
        assert ret_user['balance'] == '5',f'Error updating balance after purchase'
        
    #It must to be possible to list the ids of all itens purchased by an user
    def test_list_purchased(self):
        print('\n[[Entering test_list_purchased]]\n')
        
        asset_pack_param_1 = {'title': "Candy Crush Sprites",
                        'description': "Pixel art-styled sprites intended for use in a Candy Crush-like game project.",
                        'web_address': "http://www.archive.com/3726746273/candy_crush_sprites.zip"}
        
        asset_pack_param_2 = {'title': "3D Cars",
                        'description': "Includes 25 racing car models in Blender format.",
                        'web_address': "http://www.archive.com/3726746273/Racing_car_models.zip"}
        
        user_param = {'name':'Fran da Silva Sauro',
                      'password':"123456"
                      }
        
        user_id = self._user_dao.create_item(user_param)

        asset_pack_id_1 = self._asset_pack_dao.create_item(asset_pack_param_1)
        asset_pack_id_2 = self._asset_pack_dao.create_item(asset_pack_param_2)
        
        self._purchase.purchase_asset_pack(user_id,asset_pack_id_1)
        self._purchase.purchase_asset_pack(user_id,asset_pack_id_2)

        purchased_list = self._purchase.get_purchased_list(user_id)
        
        assert asset_pack_id_1 in purchased_list,f'Error listing purchased asset packs'
        assert asset_pack_id_2 in purchased_list,f'Error listing purchased asset packs'

    #it must to be possible to purchase credits and increase user balance
    def test_purchase_credits(self):
        print('\n[[Entering test_purchase_credits]]\n')
        
        user_param = {'name':'Bobby',
                      'password':"nicepassword",
                      'balance':'10'
                      }

        user_id = self._user_dao.create_item(user_param)
        
        result = self._purchase.purchase_credits(user_id,10)
        assert result == return_values.SUCCESS,f'Error purchasing credits'
        
        ret_user = self._user_dao.read_item(user_id)
        assert ret_user['balance'] == '20',f'Error updating balance after credit purchase'
        
    # Purchase must fail if user has not enough credits to purchase an item
    def test_purchase_failure(self):
        print('\n[[Entering test_purchase_failure]]\n')
        
        asset_pack_param = {'title': "Ultra human",
                        'description': "Ultra realistic human 3D models",
                        'web_address': "http://www.archive.com/3726746dsf273/ultra_models.zip",
                        'cost':'50'}
                        
        
        user_param = {'name':'Aleatory Guy',
                      'password':"password",
                      'balance':'10'
                      }

        user_id = self._user_dao.create_item(user_param)
        asset_pack_id = self._asset_pack_dao.create_item(asset_pack_param)

        result = self._purchase.purchase_asset_pack(user_id,asset_pack_id)
        assert result == return_values.NOT_ENOUGH_BALANCE_FOR_PURCHASE,f'Error User purchased without enough credits'

    def teardown_class(self):
        print('\n[[Entering teardown_class]]\n')
        
        if self._skip_teardown:
            print('\n Teardown skipped \n')
            return 

        self._user_dao.delete_table()
        self._asset_pack_dao.delete_table()
        
