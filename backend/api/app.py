from chalice import Chalice, AuthResponse
from chalicelib.DAO import user_dao, asset_pack_dao
from chalicelib.controllers import purchase_controller
from chalicelib.definitions import database_defs

app = Chalice(app_name='api')

#Read table names from enviromnent variables
#"Here, we are not using the Python 'os' library to read environment variables.
#'database_defs.Table_Defs' allows us to standardize the names of environment variables for both production and testing.

table_defs = database_defs.Table_Defs()
table_names = table_defs.get_public_table_names()  
TABLE_USER_NAME = table_names['user_table']
TABLE_ASSETS_NAME =  table_names['asset_packet_table']

@app.route('/')
def index():
    return {'Bem vindo a aplicação': 'GameAssetsStore'}

@app.route('/register', methods=['POST'])
def user_register():
    dao = user_dao.User_DAO(TABLE_USER_NAME)
    body = app.current_request.json_body
    response = dao.create_item(body)
    print(response)
    return {'Response': response}

@app.route('/login', methods=['POST'])
def login():
    dao = user_dao.User_DAO(TABLE_USER_NAME)
    body = app.current_request.json_body
    response = dao.user_login(body['name'], body['password'])

    return {'Response': response , 'Token': response}


@app.authorizer()
def jwt_auth(auth_request):
    dao = user_dao.User_DAO(TABLE_USER_NAME)
    token = auth_request.token
    decoded = dao.decode_jwt_token(token)
    try:
        return AuthResponse(routes=['*'], principal_id=decoded['sub'])
    except:
        return {'Response': 'Invalid token'}


"""
    if token is None:
        raise CognitoUnauthorizedError(auth_request.token)
    return AuthResponse(routes=['*'], principal_id=token,
                        context={'user': token})
"""

def get_authorized_username(current_request):
    return current_request.context['authorizer']['principalId']

@app.route('/assets', methods=['GET'])
def get_assets():
    dao = asset_pack_dao.Asset_pack_DAO(TABLE_ASSETS_NAME)
    response = dao.read_all_items()
    return {'Response': response}

@app.route('/assets', methods=['POST'])
def create_asset():
    dao = asset_pack_dao.Asset_pack_DAO(TABLE_ASSETS_NAME)
    body = app.current_request.json_body
    response = dao.create_item(body)
    return {'Response': response}


@app.route('/assets/{asset_id}', methods=['GET'], authorizer=jwt_auth)
def get_asset():
    
    return {'Bem vindo a aplicação': 'GameAssetsStore'}


@app.route('/asset/{asset_id}/purchase', methods=['POST'], authorizer=jwt_auth)
def buy_assets(asset_id):

    userdao = user_dao.User_DAO(TABLE_USER_NAME)
    userId = userdao.create_item_id({ "name": app.current_request.context['authorizer']['principalId']})
    purchase = purchase_controller.Purchase_Controller()
    response = purchase.purchase(userId, asset_id)
    return {'Response': response}

#Utilizado anteriormente para criar a tabela de assets
@app.route('/create_table', methods=['POST'])
def create_table():
    dao = asset_pack_dao.Asset_pack_DAO(TABLE_ASSETS_NAME)
    response = dao.create_table()
    print(response)
    return {'Response': response}