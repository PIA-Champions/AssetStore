from chalice import Chalice, AuthResponse, CORSConfig, Response, UnauthorizedError, BadRequestError
from chalicelib.DAO import user_dao, asset_pack_dao
from chalicelib.controllers import purchase_controller
from chalicelib.definitions import database_defs
cors_config = CORSConfig(
    allow_origin='*',
    allow_headers=['Content-Type', 'X-Amz-Date', 'Authorization', 'X-Api-Key', 'X-Amz-Security-Token', 'Authorization'],
    max_age=600,
    allow_credentials=True
)

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

@app.route('/register', methods=['POST'], cors=cors_config)
def user_register():
    dao = user_dao.User_DAO(TABLE_USER_NAME)
    body = app.current_request.json_body
    response = dao.create_item(body)
    if response == 'ITEM_ALREADY_EXISTS':
        raise BadRequestError('User already exists')
    return {'Response': response}

@app.route('/login', methods=['POST'], cors=cors_config)
def login():
    dao = user_dao.User_DAO(TABLE_USER_NAME)
    body = app.current_request.json_body
    response = dao.user_login(body['name'], body['password'])
    
    if isinstance(response, dict):
        if response.get('jwt', False):
            return Response(body={'Response': 'SUCESS' , 'Token': response['jwt'], 'id':response['user_id']})
    else:
        raise UnauthorizedError('Invalid username or password')


@app.authorizer()
def jwt_auth(auth_request):
    dao = user_dao.User_DAO(TABLE_USER_NAME)
    token = auth_request.token
    decoded = dao.decode_jwt_token(token)
    try:
        return AuthResponse(routes=['*'], principal_id=decoded['sub'])
    except:
        return {'Response': 'Invalid token'}

def get_authorized_username(current_request):
    return current_request.context['authorizer']['principalId']

@app.route('/assets', methods=['GET'], cors=cors_config)
def get_assets():
    dao = asset_pack_dao.Asset_pack_DAO(TABLE_ASSETS_NAME)
    response = dao.read_all_items()
    return {'Response': response}

@app.route('/assets/search', methods=['GET'], cors=cors_config)
def search_assets():
    dao = asset_pack_dao.Asset_pack_DAO(TABLE_ASSETS_NAME)
    keyword = app.current_request.query_params.get('keyword', '')
    # Define the attributes you want to search on
    attribute_names = ['title', 'description', 'web_address']  # Add more attributes as needed
    # Call the search_items_by_keyword method from DAO
    response = dao.search_itens_by_keyword(keyword, attribute_names)
    return {'Response': response}

@app.route('/assets', methods=['POST'], cors=cors_config)
def create_asset():
    dao = asset_pack_dao.Asset_pack_DAO(TABLE_ASSETS_NAME)
    body = app.current_request.json_body
    response = dao.create_item(body)
    return {'Response': response}


@app.route('/assets/{asset_id}', methods=['GET'], authorizer=jwt_auth, cors=cors_config)
def get_asset():
    
    return {'Bem vindo a aplicação': 'GameAssetsStore'}


@app.route('/asset/{asset_id}/purchase', methods=['POST'], authorizer=jwt_auth, cors=cors_config)
def buy_assets(asset_id):

    userdao = user_dao.User_DAO(TABLE_USER_NAME)
    userId = userdao.create_item_id({ "name": app.current_request.context['authorizer']['principalId']})
    purchase = purchase_controller.Purchase_Controller()
    response = purchase.purchase_asset_pack(userId, asset_id)
    return {'Response': response}

@app.route('/user/{user_id}/buy-credits', methods=['POST'], cors=cors_config, authorizer=jwt_auth)
def buy_credits(user_id):
    
    body = app.current_request.json_body
    coins_to_buy = body.get('credits_to_buy', 0)
    purchase = purchase_controller.Purchase_Controller()
    response = purchase.purchase_credits(user_id,coins_to_buy)
    return {'Response': response}

@app.route('/user/{user_id}', methods=['GET'], cors=cors_config)
def get_user(user_id):
    userdao = user_dao.User_DAO(TABLE_USER_NAME)
    response = userdao.read_item(user_id)
    del response['password']
    return {'Response': response}

@app.route('/user/{user_id}', methods=['PUT'], cors=cors_config, authorizer=jwt_auth)
def update_user(user_id):
    userdao = user_dao.User_DAO(TABLE_USER_NAME)
    body = app.current_request.json_body
    response = userdao.update_item(user_id, body)
    return {'Response': response}

@app.route('/user/{user_id}', methods=['DELETE'], cors=cors_config, authorizer=jwt_auth)
def delete_user(user_id):
    userdao = user_dao.User_DAO(TABLE_USER_NAME)
    response = userdao.delete_item(user_id)
    return {'Response': response}

#Utilizado anteriormente para criar a tabela de assets
@app.route('/create_table/assets', methods=['POST'])
def create_table():
    dao = asset_pack_dao.Asset_pack_DAO(TABLE_ASSETS_NAME)
    response = dao.create_table()
    return {'Response': response}

@app.route('/create_table/users', methods=['POST'])
def create_table():
    dao = user_dao.User_DAO(TABLE_USER_NAME)
    response = dao.create_table()
    return {'Response': response}