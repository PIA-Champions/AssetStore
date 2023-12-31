from chalicelib.DAO import user_dao,asset_pack_dao
from chalicelib.definitions import database_defs, return_values

class Purchase_Controller:
    def __init__(self):
        table_defs = database_defs.Table_Defs()
        table_names = table_defs.get_public_table_names()
        user_table_name = table_names['user_table']
        asset_packet_table_name = table_names['asset_packet_table']
        self.set_table_names(user_table_name, asset_packet_table_name)

    
    def set_table_names(self, user_table_name, asset_pack_table_name):
        self._u_dao = user_dao.User_DAO(user_table_name)
        self._p_dao = asset_pack_dao.Asset_pack_DAO(asset_pack_table_name)


    # purchase asset pack reffered by asset_pack_id
    # add the refered assed to user's purchased_asset_packs
    # return valuse:
    #   SUCCESS
    #   ITEM_NOT_FOUD: USER
    #   ITEM_NOT_FOUND: ASSET_PACK
    def purchase_asset_pack(self,user_id,asset_pack_id):

        
        user_data = self._u_dao.read_item(user_id)
        if not self._u_dao.validate_item(user_data):
            return return_values.ITEM_NOT_FOUND + ': USER'
        
        purchased_asset_packs = user_data.get('purchased_asset_packs',[])
        

        for purchased in purchased_asset_packs:
            if purchased == asset_pack_id:
                return return_values.ITEM_ALREADY_PURCHASED

        asset_pack_data = self._p_dao.read_item(asset_pack_id) 
        if not self._p_dao.validate_item(asset_pack_data):
            return return_values.ITEM_NOT_FOUND + ': ASSET_PACK' 

        
        #Prossess asset pack purchasing business rules
        balance = float(user_data.get('balance','0'))
        cost = float (asset_pack_data.get('cost','0'))

        if cost > balance:
            return return_values.NOT_ENOUGH_BALANCE_FOR_PURCHASE
            
        user_data['balance'] = str(balance - cost)
        purchased_asset_packs.append(asset_pack_id)
        user_data['purchased_asset_packs'] =  purchased_asset_packs
        self._u_dao.update_item(user_id,user_data)
        
        return return_values.SUCCESS
    
    # Process purchasing of credits
    def purchase_credits(self,user_id,credits):
        user_data = self._u_dao.read_item(user_id)
        if not self._u_dao.validate_item(user_data):
            return return_values.ITEM_NOT_FOUND + ': USER'
        converted_credits = float(credits)
        if int(converted_credits) < 0:
            return return_values.INVALID_INPUT_DATA

        # Process credit purchasing business rulles
        # [TODO] Validation and dept according with payment system 

        current_balance = float(user_data['balance'])
        user_data['balance'] = str(current_balance + converted_credits)
        
        self._u_dao.update_item(user_id,user_data)    
        return return_values.SUCCESS
    
    # Return a list of asset packs ids purchased by the user
    # May also return 
    # ITEM_NOT_FOUND: USER
    def get_purchased_list(self,user_id):        
        user_data = self._u_dao.read_item(user_id)
        
        if not self._u_dao.validate_item(user_data):
            return return_values.ITEM_NOT_FOUND + ': USER'
        
        return user_data.get('purchased_asset_packs',[])
        
