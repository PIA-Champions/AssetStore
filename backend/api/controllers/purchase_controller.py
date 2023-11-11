from DAO import user_dao,asset_pack_dao
from definitions import database_defs, return_values
class Purchase_Controller:
    def __init__(self):
        self.set_table_names(database_defs.USER_TABLE_NAME, database_defs.ASSET_PACK_TABLE_NAME)

    
    def set_table_names(self, user_table_name, asset_pack_table_name):
        self._u_dao = user_dao.User_DAO(user_table_name)
        self._p_dao = asset_pack_dao.Asset_pack_DAO(asset_pack_table_name)


    # purchase asset pack reffered by asset_pack_id
    # add the refered assed to user's purchased_asset_packs
    # return valuse:
    #   SUCCESS
    #   ITEM_NOT_FOUD: USER
    #   ITEM_NOT_FOUND: ASSET_PACK
    def purchase(self,user_id,asset_pack_id):
        
        user_data = self._u_dao.read_item(user_id)
        asset_pack_data = self._p_dao.read_item(asset_pack_id) 
        
        if not self._u_dao.validate_item(user_data):
            return return_values.ITEM_NOT_FOUND + ': USER'
        if not self._p_dao.validate_item(asset_pack_data):
            return return_values.ITEM_NOT_FOUND + ': ASSET_PACK' 

        purchased_asset_packs = user_data.get('purchased_asset_packs',[])

        # [TODO] Prossess purchasing business rules 
        
        purchased_asset_packs.append(asset_pack_id)

        user_update_data= {
            'name':user_data['name'],
            'password': user_data['password'],
            'purchased_asset_packs': purchased_asset_packs
        }

        self._u_dao.update(user_id,user_update_data)
        return return_values.SUCCESS

    # Return a list of asset packs ids purchased by the user
    # May also return 
    # ITEM_NOT_FOUND: USER
    def list_purchased(self,user_id):        
        user_data = self._u_dao.read_item(user_id)
        
        if not self._u_dao.validate_item(user_data):
            return return_values.ITEM_NOT_FOUND + ': USER'
        
        return user_data.get('purchased_asset_packs',[])
        
