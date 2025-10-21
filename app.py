from flask import Flask
from database import db
from routes import app_routes
from errors import errors
from auth_routes import auth_routes

app = Flask(__name__)

#CONFIGURA O BANCO DE DADOS:

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///financas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'uma_chave_muito_secreta'

#INICIAR O BANCO COM O FLASK:

db.init_app(app)

#RESGITRO DE ROTAS:

app.register_blueprint(app_routes) #REGISTRO DE ROTAS
app.register_blueprint(errors) #REGISTRAR ERROS
app.register_blueprint(auth_routes) #REGISTRO DE LOGIN E REGISTRO

#CRIAR O BANCO DE DADOS:

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)