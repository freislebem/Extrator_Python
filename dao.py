#from jogoteca import Jogo, Usuario
import Enderecos, Usuario

SQL_DELETA_ENDERECO = 'delete from endereco_web where id = %s'
SQL_ENDERECO_POR_ID = 'SELECT id, nomeSite, enderecoSite, palavrasChave from endereco_web where id = %s'
SQL_USUARIO_POR_ID = 'SELECT id, nome, senha from usuario where id = %s'
SQL_ATUALIZA_ENDERECO = 'UPDATE endereco_web SET nomeSite=%s, enderecoSite=%s, palavrasChave=%s where id = %s'
SQL_BUSCA_ENDERECO = 'SELECT id, nomeSite, enderecoSite, palavrasChave from endereco_web'
SQL_CRIA_ENDERECO = 'INSERT into endereco_web (nomeSite, enderecoSite, palavrasChave) values (%s, %s, %s)'


class EnderecoDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, endereco_web):
        cursor = self.__db.connection.cursor()

        if (endereco_web.id):
            cursor.execute(SQL_ATUALIZA_ENDERECO, (endereco_web.nomeSite, endereco_web.enderecoSite, endereco_web.palavras_chave, endereco_web.id))
        else:
            cursor.execute(SQL_CRIA_ENDERECO, (endereco_web.nomeSite, endereco_web.enderecoSite, endereco_web.palavrasChave))
            endereco_web.id = cursor.lastrowid
        self.__db.connection.commit()
        return endereco_web

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_ENDERECO)
        enderecos = traduz_enderecos(cursor.fetchall())
        return enderecos

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_ENDERECO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Enderecos(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_ENDERECO, (id, ))
        self.__db.connection.commit()


class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def buscar_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario


def traduz_enderecos(enderecos):
    def cria_endereco_com_tupla(tupla):
        return Enderecos(tupla[1], tupla[2], tupla[3], id=tupla[0])
    return list(map(cria_endereco_com_tupla, enderecos))


def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2])
