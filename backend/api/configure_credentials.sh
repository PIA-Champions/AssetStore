# Set environment variables
export TABLE_USER_NAME=user_table 
export TABLE_ASSETS_NAME=asset_pack_table
export TEST_TABLE_USER_NAME=test_user_table
export TEST_TABLE_ASSETS_NAME=test_asset_pack_table
configFile="$HOME/.aws/config"
# Check if config file exists
if [ -e $configFile ]; then
    echo "File $configFile allready exists."
else
    # Create the config file
     cp default_Credentials.txt $configFile
     echo "$configFile created."
fi
nano $configFile
