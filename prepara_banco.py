import MySQLdb

print('Conectando...')
# conn = MySQLdb.connect(user='root', passwd='admin', host='127.0.0.1', port=3306)
conn = MySQLdb.connect(user='root', passwd='', host='127.0.0.1', port=3306)

# Descomente se quiser desfazer o banco...
conn.cursor().execute("DROP DATABASE `extrator_python`;")
conn.commit()

criar_tabelas = '''SET NAMES utf8;
    CREATE DATABASE `extrator_python` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
    USE `extrator_python`;
    CREATE TABLE `endereco_web` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nomeSite` varchar(40) COLLATE utf8_bin NOT NULL,
      `enderecoSite` varchar(50) COLLATE utf8_bin NOT NULL,
      `palavrasChave` varchar(100) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    CREATE TABLE `usuario` (
      `id` varchar(8) COLLATE utf8_bin NOT NULL,
      `nome` varchar(20) COLLATE utf8_bin NOT NULL,
      `senha` varchar(8) COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''

conn.cursor().execute(criar_tabelas)

# inserindo usuarios
cursor = conn.cursor()
cursor.executemany(
    'INSERT INTO extrator_python.usuario (id, nome, senha) VALUES (%s, %s, %s)',
    [
        ('Freislebem', 'Denis Freislebem', 'F123'),
        ('Bacon', 'Rafael Bacon', 'B123'),
        ('Tayze', 'Tayze Couto', 'T123')
    ])

cursor.execute('select * from extrator_python.usuario')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
cursor.executemany(
    'INSERT INTO extrator_python.endereco_web (nomeSite, endereco_site, palavras_chave) VALUES (%s, %s, %s)',
    [
        ('Uol', 'http://www.uol.com.br', 'moda, coleção, riachuelo, marisa, pernanbucanas, roupas, look'),
        ('Globo', 'http://www.globo.com', 'moda, coleção, riachuelo, marisa, pernanbucanas, roupas, look'),
        ('Ig', 'http://www.ig.com.br', 'moda, coleção, riachuelo, marisa, pernanbucanas, roupas, look'),
    ])

cursor.execute('select * from extrator_python.enderecos_web')
print(' -------------  Enderecos_Web:  -------------')
for enderecos_web in cursor.fetchall():
    print(enderecos_web[1])

# commitando senão nada tem efeito
conn.commit()
cursor.close()
