#Define names and parameters for the database
import os
# This class provides the database table names 
# that must be previouslly set as . environment variables.
# This allows the definition of tables for production and testing
#
# TABLE_USER_NAME - User table for public (production) use
# TABLE_ASSETS_NAME - Asset pack table for public use
# TEST_TABLE_USER_NAME - User table for unity testing
# TEST_TABLE_ASSETS_NAME - Asset pack table for unity testing

class Table_Defs:
    def __init__(self):
        
        self.public_tables = {
            'user_table':os.getenv('TABLE_USER_NAME'),
            'asset_packet_table':os.getenv('TABLE_ASSETS_NAME')
        }

        self.test_tables = {
            'user_table':os.getenv('TEST_TABLE_USER_NAME'),
            'asset_packet_table':os.getenv('TEST_TABLE_ASSETS_NAME')
        }

    def get_public_table_names(self):
        print(self.public_tables)
        return self.public_tables

    def get_test_table_names(self):
        return self.test_tables
