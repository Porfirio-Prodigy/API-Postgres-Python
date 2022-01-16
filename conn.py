import psycopg2

def connection():
    con = psycopg2.connect(host='localhost', database='notas',user='postgres', password='j9p3e3ysk')
    return con

con = connection()
cur = con.cursor()

def init():
    sql = """CREATE TABLE IF NOT EXISTS alunos(
    idAluno bigint PRIMARY KEY,
    nome varchar(30));"""

    sql2 = """CREATE TABLE IF NOT EXISTS notas (
    idNotas bigint PRIMARY KEY,
    idAlunoFK bigint,
    n1 int,
    n2 int,
    n3 int,
    n4 int,
    FOREIGN KEY (idAlunoFK) REFERENCES alunos (idAluno)
    );"""

    cur.execute(sql)
    cur.execute(sql2)
    con.commit()


#Adicional nota aos alunos
def insert(id, nome, n1, n2, n3, n4):
    id = id
    nome = nome
    n1, n2, n3, n4 = n1, n2, n3, n4   
        
    sql = "insert into alunos values ({}, '{}')".format(id, nome)
    sql2 = "insert into notas values ({}, {}, {}, {}, {}, {})".format(id, id, n1, n2, n3, n4)
    cur.execute(sql)
    cur.execute(sql2)
    con.commit()

#Get Completo
def get_all():
    cur.execute('select idAluno, nome, n1, n2, n3, n4 from alunos inner join notas b on idAluno = idAlunoFK')
    lista_completa = cur.fetchall()
    return lista_completa

def update(id):
    id = id
    print(id)
    sql = 'select idAluno, nome, n1, n2, n3, n4 from alunos inner join notas b on idAluno = idAlunoFK where idAlundo = {}'.format(id)
    cur.execute(sql)
    lista_completa = cur.fetchall()
    return lista_completa


