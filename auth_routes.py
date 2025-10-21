from flask import Blueprint, request, jsonify, current_app as app
from database import db
from models import Usuario
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

auth_routes = Blueprint('auth_routes', __name__)

#REGISTRO:

@auth_routes.route('/register', methods=['POST'])
def register():
    dados = request.get_json()
    if not dados or 'username' not in dados or 'password' not in dados:
        return jsonify({"erro": "Username e senha são obrigatórios."}), 400
    
    usuario_existente = Usuario.query.filter_by(username=dados['username']).first()
    if usuario_existente:
        return jsonify({"erro": "Usuário já existe."}), 400

    hashed_password = generate_password_hash(dados['password'], method='pbkdf2:sha256')
    novo_usuario = Usuario(username=dados['username'], password=hashed_password)
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({"mensagem": "Usuário criado com sucesso!"}), 201

#LOGIN:

@auth_routes.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    if not dados or 'username' not in dados or 'password' not in dados:
        return jsonify({"erro": "Username e senha são obrigatórios"}), 400
    
    usuario = Usuario.query.filter_by(username=dados['username']).first()
    if not usuario or not check_password_hash(usuario.password, dados['password']):
        return jsonify({"erro": "Usuário ou senha incoretos."}), 401
    
    token = jwt.encode({
        'id' : usuario.id,
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({
        "token": token,
        "expira_em": "1 hora"
        })