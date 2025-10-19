from database import db

#TABELA DE TRASAÇÕES:

class Transacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(100))

    def __repr__(self):
        return f'<Transacao {self.tipo} - {self.valor}>' 
    
#TABELA DE USUÁRIOS:
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)