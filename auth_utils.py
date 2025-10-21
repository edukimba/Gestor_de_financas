from functools import wraps
from flask import request, jsonify, current_app as app
import jwt
from models import Usuario

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({"erro": "Token não fornecido."}), 401
        try:
            dados = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            usuario = Usuario.query.get(dados['id'])
        except jwt.ExpiredSignatureError:
            return jsonify({"erro": "Token expirado."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"erro": "Token inválido."}), 401
        
        return f(usuario, *args, **kwargs)
    
    return decorated



