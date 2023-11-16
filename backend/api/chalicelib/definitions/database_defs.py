#Define names and parameters for the database
import os

class Database_Defs:
    __init__(self):
        
        self.public_tables = {
            'user_table':os.getenv('TABLE_USER_NAME'),
            'asset_packet_table':os.getenv('TABLE_ASSETS_NAME')
        }

        self.test_tables = {
            'user_table':os.getenv('TEST_TABLE_USER_NAME'),
            'asset_packet_table':os.getenv('TEST_TABLE_ASSETS_NAME')
        }

    get_public_tables(self):
        return self.public_tables

    get_test_tables(self):
        return self.test_tables
