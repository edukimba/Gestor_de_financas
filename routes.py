from flask import Blueprint, request, jsonify
from database import db
from models import Transacao

app_routes = Blueprint('app_routes', __name__)

#CRIAR NOVA TRANSAÇÃO:

@app_routes.route('/transacoes', methods=['POST'])
def criar_transacao():
    dados = request.get_json()
    nova = Transacao(
        tipo=dados['tipo'],
        valor=dados['valor'],
        descricao= dados.get('descricao', '')
    )
    db.session.add(nova)
    db.session.commit()
    return jsonify({'mensagem': 'Transação criada com sucesso!'}), 201

#LISTAR TRANSAÇÕES:

@app_routes.route('/transacoes', methods=['GET']) 
def listar_transacoes():
    transacoes = Transacao.query.all()
    resultado = [
        {'id': t.id, 'tipo': t.tipo, 'valor': t.valor, 'descricao': t.descricao}
        for t in transacoes
        ]
    
    return jsonify(resultado)

#DELETAR UM TRASAÇÃO:

@app_routes.route('/transacoes/<int:id>', methods=['DELETE'])
def deletar_transacao(id):
    transacao = Transacao.query.get(id)
    if transacao:
        db.session.delete(transacao)
        db.session.commit()
        return jsonify({'mensagem': 'Transacao deletada com sucesso!'})
    return jsonify({'erro': 'Transação não encontrada'}), 404

