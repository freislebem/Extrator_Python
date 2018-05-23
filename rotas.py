from flask import Flask, render_template, request, redirect, session, flash, url_for
from Enderecos import Enderecos
from Usuario import Usuario

app = Flask(__name__)
app.secret_key = 'misere'

usuario1 = Usuario('Freislebem', 'Denis Freislebem', '1234')
usuario2 = Usuario('Bacon', 'Rafael Bacon', '1234')
usuario3 = Usuario('Tayze', 'Tayze Couto', '1234')

usuarios = {usuario1.id: usuario1, usuario2.id: usuario2, usuario3.id: usuario3}

lista = []

site1 = Enderecos("UOL", "http://www.uol.com.br", "cerveja, cervejaria, lupulo")
site2 = Enderecos('GLOBO', 'http://www.globo.com', 'cerveja, cervejaria, bar brahma, skol')
lista = [site1, site2]

@app.route('/')
def index():
    return render_template('index.html', titulo = 'WEB SCRAPER')

@app.route('/criarLink')
def criarLink():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Para acessar a página solicitada é necessário fazer login')
        return redirect(url_for('login', proxima = url_for('criarLink')))#redireciona direto para o metodo junto com o argumento proxima (também passando o método)
    return render_template('criarLink.html', titulo = 'Cadastro de Endereço para extração')

@app.route('/listarLink', methods = ['POST',])
def listarLink():

    nomeSite = request.form['nomeSite']
    enderecoSite = request.form['enderecoSite']
    palavrasChave = request.form['palavrasChave']

    novo = Enderecos(nomeSite, enderecoSite, palavrasChave)
    lista.append(novo)

    #return render_template('listarLink.html', titulo = 'Lista de Links e Palavras-chave para extração', listaLinks = lista)
    return redirect(url_for('listar'))

@app.route('/listar')
def listar():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Para acessar a página solicitada é necessário fazer login')
        return redirect(url_for('login', proxima = url_for('listar')))#redireciona para o login junto com o argumento "proxima pagina"
    return render_template('listarLink.html', titulo='Lista de Links e Palavras-chave para extração', listaLinks=lista)

@app.route('/Admin')
def Admin():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Para acessar a página solicitada é necessário fazer login')
        return redirect(url_for('login', proxima = url_for('Admin')))#redireciona para o login junto com o argumento "proxima pagina"
    return render_template('admin.html', titulo = 'ADMINISTRAÇÃO')

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = request.form['usuario']
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            # return redirect('/{}'.format(proxima_pagina))
            return redirect(proxima_pagina)
        else:
            flash('Login ou senha inválido, tente novamente!')
            #return redirect('/login')
            return redirect(url_for('login'))
    else:
        flash('Login ou senha inválido, tente novamente!')
        # return redirect('/login')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    #return redirect('/login')
    return redirect(url_for('login'))

app.run(debug=True)