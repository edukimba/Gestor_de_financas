from flask import Blueprint, jsonify

#TRATAMENTO DE ERROS:

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def not_found_error(error):
    return jsonify({'erro': 'Rota não encontrada!'}), 404

@errors.app_errorhandler(400)
def bad_request_error(error):
    return jsonify({'erro': 'Requisição inválida!'}), 400

@errors.app_errorhandler(500)
def internal_error(error):
    return jsonify({'erro': 'Erro interno no servidor.'}), 500

