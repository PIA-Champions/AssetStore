from DAO import user_dao,asset_pack_dao
from definitions import database_defs, return_values
class Purchase_Controller:
    
    def purchase(self,user_id,asset_pack_id):
        u_dao = user_dao.User_DAO(database_defs.USER_TABLE_NAME)
        p_dao = asset_pack_dao.Asset_pack_DAO(database_defs.ASSET_PACK_TABLE_NAME)

        user_data = u_dao.read_item(user_id)
        asset_pack_data = p_dao.read_item(asset_pack_id) 
        
        if not u_dao.validate_item(user_data):
            return return_values.ITEM_NOT_FOUND + ': USER'
        if not p_dao.validate_item(asset_pack_data):
            return return_values.ITEM_NOT_FOUND + ': ASSET_PACK' 

        purchased_asset_packs = user_data.get('purchased_asset_packs',[])
        purchased_asset_packs.append(asset_pack_id)

        user_update_data= {
            'name':user_data['name'],
            'password': user_data['password'],
            'purchased_asset_packs': purchased_asset_packs
        }

        u_dao.update(user_id,user_update_data)
        return return_values.SUCCESS

        
