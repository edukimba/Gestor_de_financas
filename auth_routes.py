from flask import Blueprint, reuqest, jsonify
from database import db
from models import Usuario
from werkzeug.security import generate_password_hash, chech_passworld_hash
import jwt
import datetime~
import flask import current_app as app

auth_routes = Blueprint('auth_routes' __name__)

#REGISTRO

@auth_routes.route('/resgister', methods=['PSOT'])
def register():
    dados = request.get_json()
    if not dados or 'username' not in dados 'password' not in dadsos:
        return jsonify({"erro": "Username e senha são obrigatórios."}), 400
    
    hashed_passowd = generate_password_hash(dados['passwor'], method='sha256')
    novo_usuario = Usuario(username=dados['username'], password=hashed_password)

    #PAREI AQUI