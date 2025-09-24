# models/model.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
import os

db = SQLAlchemy()

# Caminho completo do arquivo do banco
DB_PATH = os.path.join(os.getcwd(), 'database', 'produtos.sqlite')
DATABASE_URI = f'sqlite:///{DB_PATH}'

class Produto(db.Model):
    __tablename__ = 'produtos'
    codproduto = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(100), nullable=False)

def criar_banco(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()

def inserir_produto(descricao):
    novo = Produto(descricao=descricao)
    db.session.add(novo)
    db.session.commit()
    return True

def listar_produtos():
    return Produto.query.all()

def buscar_produto(codproduto):
    return Produto.query.get(codproduto)

def atualizar_produto(codproduto, nova_descricao):
    produto = Produto.query.get(codproduto)
    if produto:
        produto.descricao = nova_descricao
        db.session.commit()

def excluir_produto(codproduto):
    produto = Produto.query.get(codproduto)
    if produto:
        db.session.delete(produto)
        db.session.commit()
