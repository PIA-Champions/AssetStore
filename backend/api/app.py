from chalice import Chalice, AuthResponse
from DAO import user_dao

app = Chalice(app_name='api')

@app.route('/')
def index():
    return {'Bem vindo a aplicação': 'GameAssetsStore'}
#Apenas um teste

@app.route('/user/create', methods=['POST'])
def user_create_table():
    dao = user_dao.User_DAO('Teste_user')
    response = dao.create_table()
    print(response)
    return {'Bem vindo a aplicação': 'GameAssetsStore'}

@app.route('/register', methods=['POST'])
def user_register():
    dao = user_dao.User_DAO('Teste_user')
    body = app.current_request.json_body
    response = dao.create_item(body)
    print(response)
    return {'Response': response}

@app.route('/login', methods=['POST'])
def login():
    dao = user_dao.User_DAO('Teste_user')
    body = app.current_request.json_body
    response = dao.user_login(body['name'], body['password'])

    jwt_token = dao.get_jwt_token(body['name'], body['password'])
    
    return {'Response': response , 'Token': jwt_token}


@app.authorizer()
def jwt_auth(auth_request):
    dao = user_dao.User_DAO('Teste_user')
    token = auth_request.token
    decoded = dao.decode_jwt_token(token)
    print(decoded)
    return AuthResponse(routes=['*'], principal_id=decoded['sub'])

"""
    if token is None:
        raise CognitoUnauthorizedError(auth_request.token)
    return AuthResponse(routes=['*'], principal_id=token,
                        context={'user': token})
"""

def get_authorized_username(current_request):
    return current_request.context['authorizer']['principalId']

@app.route('/assets', methods=['GET'], authorizer=jwt_auth)
def get_assets():
    return {'Bem vindo a aplicação': 'GameAssetsStore'}