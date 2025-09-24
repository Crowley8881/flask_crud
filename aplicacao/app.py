from flask import Flask, render_template, request, redirect, url_for, flash
from models import model
from forms.produto_form import ProdutoForm

import os

app = Flask(__name__)
app.secret_key = 'senha123'

def inicializar():
    if not os.path.exists('database'):
        os.makedirs('database')
    model.criar_banco(app)

@app.route('/')
def index():
    return redirect(url_for('listar'))

@app.route('/listar')
def listar():
    produtos = model.listar_produtos()
    return render_template('listar.html', produtos=produtos)

@app.route('/inserir', methods=['GET', 'POST'])
def inserir():
    form = ProdutoForm()
    if form.validate_on_submit():
        if model.inserir_produto(form.descricao.data):
            flash("Produto inserido com sucesso!", "sucesso")
            return redirect(url_for('listar'))
        else:
            flash("Erro: código duplicado.", "erro")
    return render_template('inserir.html', form=form)

@app.route('/alterar/<int:cod>', methods=['GET', 'POST'])
def alterar(cod):
    produto = model.buscar_produto(cod)
    if not produto:
        flash("Produto não encontrado.", "erro")
        return redirect(url_for('listar'))

    form = ProdutoForm(obj=produto)

    if form.validate_on_submit():
        model.atualizar_produto(cod, form.descricao.data)
        flash("Produto atualizado com sucesso!", "sucesso")
        return redirect(url_for('listar'))

    return render_template('alterar.html', form=form)

@app.route('/excluir/<int:cod>', methods=['GET', 'POST'])
def excluir(cod):
    produto = model.buscar_produto(cod)
    if not produto:
        flash("Produto não encontrado.", "erro")
        return redirect(url_for('listar'))

    if request.method == 'POST':
        model.excluir_produto(cod)
        flash("Produto excluído com sucesso!", "sucesso")
        return redirect(url_for('listar'))

    return render_template('excluir.html', produto=produto)

if __name__ == '__main__':
    inicializar()
    app.run(debug=True)
