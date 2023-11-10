import pytest
from DAO import asset_pack_dao
from DAO import user_dao 
from util import data_util
from definitions import return_values
import boto3
import time

class TestAsset_pack_DAO:
    _asset_pack_dao = None
    _user_dao = None
    _asset_pack_table_name = "test_asset_pack_table"
    _user_table_name = "test_user_table"

    def setup_class(self):
        print('\n[[Entering setup_class]]\n')
        self._asset_pack_dao = asset_pack_dao.Asset_pack_DAO(self._asset_pack_table_name)
        self._user_dao = user_dao.User_DAO(self._user_table_name)
        assert self._user_dao.create_table() == return_values.SUCCESS,f'Error creating user table'
        assert self._asset_pack_dao.create_table() == return_values.SUCCESS,f'Error creating asset pack table'
    
    #It must be possible to search asset_packs by keyword
    def test_dummy(self):
        print('\n[[Entering test_dummy]]\n')
        
    
    
    def teardown_class(self):
        print('\n[[Entering teardown_class]]\n')
        self._user_dao.delete_table()
        self._asset_pack_dao.delete_table()
        
