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

#ATUALIZAR TRANSAÇÃO:

@app_routes.route('/transacoes/<int:id>', methods=['PUT'])
def atualizar_transacao(id):
    transacao = Transacao.query.get(id)
    if not transacao:
        return jsonify({'erro': 'Transação não encontrada!'}), 404
    
    dados = request.get_json()

    transacao.tipo = dados.get('tipo', transacao.tipo)
    transacao.valor = dados.get('valor', transacao.valor)
    transacao.descricao = dados.get('descricao', transacao.descricao)

    db.session.commit()
    return jsonify({'mensagem': 'Transação atualizada com sucesso!'})

#CALCULAR SALDO:

@app_routes.route('/saldo', methods=['GET'])
def calcular_saldo():
    transacoes = Transacao.query.all()

    total_entradas = sum(t.valor for t in transacoes if t.tipo == 'entrada')
    total_saidas = sum(t.valor for t in transacoes if t.tipo == 'saidas') 
    saldo = total_entradas - total_saidas

    return jsonify({
        'entradas': total_entradas,
        'saidas': total_saidas,
        'saldo_total': saldo
    })