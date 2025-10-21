from flask import Blueprint, request, jsonify
from database import db
from models import Transacao
from auth_utils import token_required

app_routes = Blueprint('app_routes', __name__)

#CRIAR NOVA TRANSAÇÃO:

@app_routes.route('/transacoes', methods=['POST'])
@token_required
def criar_transacao(usuario):
    try:
        dados = request.get_json()

        if not dados:
            return jsonify({"erro": "Nenhum dado enviado. Envie um JSON válido."}), 400
        
        if 'tipo' not in dados or 'valor' not in dados:
            return jsonify({"erro": "Os campos 'tipo' são obrigatórios. "}), 400
        
        
        try:
            valor = float(dados['valor'])
        except ValueError:
            return jsonify({"erro": "o campo 'valor' deve ser númerico." }), 400
        
        nova = Transacao(
            tipo=dados['tipo'],
            valor=valor,
            descricao=dados.get('descricao', '')
        )

        db.session.add(nova)
        db.session.commit()

        return jsonify({"mensagem": "Transação criada com sucesso!"}), 201
    
    except Exception as e:

        return jsonify({"erro": f"Ocorreu um erro interno: {str(e)}"}), 500


#LISTAR TIPOS DE TRANSAÇÕES:

@app_routes.route('/transacoes', methods=['GET'])
def listar_tipos_transacoes():
    tipo = request.args.get('tipo')  # entrada, saida ou None

    if tipo in ["entrada", "saida"]:
        transacoes_filtradas = [t for t in Transacao.query.all() if t.tipo == tipo]
    else:
        transacoes_filtradas = Transacao.query.all()

    resultado = [
        {"id": t.id, "tipo": t.tipo, "valor": t.valor, "descricao": t.descricao}
        for t in transacoes_filtradas
    ]

    return jsonify(resultado), 200

#DELETAR UM TRASAÇÃO:

@app_routes.route('/transacoes/<int:id>', methods=['DELETE'])
def deletar_transacao(id):
    try:
        transacao = Transacao.query.get(id)
        if not transacao:
            return jsonify({"erro": "Transação não encontrada!"}), 404
        
        db.session.delete(transacao)
        db.session.commit()

        return jsonify({"mensagem": "Transação deletada com sucesso!"}), 200

    except Exception as e:
        return jsonify({"erro": f"Ocorreu um erro interno: {str(e)}"}), 500

#ATUALIZAR TRANSAÇÃO:

@app_routes.route('/transacoes/<int:id>', methods=['PUT'])
def atualizar_transacao(id):
    transacao = Transacao.query.get(id)
    if not transacao:
        return jsonify({"erro": "Transação não encontrada!"}), 404
    
    dados = request.get_json()

    transacao.tipo = dados.get('tipo', transacao.tipo)
    transacao.valor = dados.get('valor', transacao.valor)
    transacao.descricao = dados.get('descricao', transacao.descricao)

    db.session.commit()

    return jsonify({"mensagem": "Transação atualizada com sucesso!"}), 201

#CALCULAR SALDO:

@app_routes.route('/saldo', methods=['GET'])
def calcular_saldo():
    transacoes = Transacao.query.all()

    total_entradas = sum(t.valor for t in transacoes if t.tipo == 'entrada')
    total_saidas = sum(t.valor for t in transacoes if t.tipo == 'saida') 
    saldo = total_entradas - total_saidas

    return jsonify({
        'entradas': total_entradas,
        'saidas': total_saidas,
        'saldo_total': saldo
    })

#LISTAR TRANSAÇÕES:

@app_routes.route('/transacoes', methods=['GET'])
def listar_transacoes():
    try:
        transacoes = Transacao.query.all()
        resultado = []
        for t in transacoes:
            resultado.append({
                "id": t.id,
                "tipo": t.tipo,
                "valor": t.valor,
                "descricao": t.descricao
                })
            
        return jsonify(resultado), 200
    
    except Exception as e:
        return jsonify({"erro": f"Ocorreu um erro interno: {str(e)}"}), 500
