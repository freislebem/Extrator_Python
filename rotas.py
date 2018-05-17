from flask import Flask, render_template, request, redirect
from Enderecos import Enderecos

app = Flask(__name__)

lista = []

site1 = Enderecos("UOL", "http://www.uol.com.br", "cerveja, cervejaria, lupulo")
site2 = Enderecos('GLOBO', 'http://www.globo.com', 'cerveja, cervejaria, bar brahma, skol')
lista = [site1, site2]

@app.route('/')
def index():
    return render_template('index.html', titulo = 'MISERÊ DO QUEIJO')

@app.route('/criarLink')
def criarLink():
    return render_template('criarLink.html', titulo = 'Cadastro de Endereço para extração')

@app.route('/listarLink', methods = ['POST',])
def listarLink():

    nomeSite = request.form['nomeSite']
    enderecoSite = request.form['enderecoSite']
    palavrasChave = request.form['palavrasChave']

    novo = Enderecos(nomeSite, enderecoSite, palavrasChave)
    lista.append(novo)

    #return render_template('listarLink.html', titulo = 'Lista de Links e Palavras-chave para extração', listaLinks = lista)
    return redirect('/listar')

@app.route('/listar')
def listar():
    return render_template('listarLink.html', titulo='Lista de Links e Palavras-chave para extração', listaLinks=lista)

@app.route('/Admin')
def Admin():
    return render_template('admin.html', titulo = 'ADMINISTRAÇÃO')

app.run(debug=True)