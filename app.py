from email import message
from flask import Flask, render_template, request, url_for, redirect, json
import conn

app = Flask(__name__, template_folder='public')
port = 5000

@app.route("/")
def index():
    conn.init()
    return render_template('index.html')

@app.route("/create")
def create():
    
    return render_template('index.html', message="Tabela criada com sucesso")

@app.route("/listar", methods=['GET'])
def listar():
    id = json.dumps(request.args)
    id = json.loads(id)
    
    con = conn.connection()
    cur = con.cursor()
    
    try:
        # Alunos
        sql = str("select idAluno, nome from alunos where idAluno = {}".format(id["idAluno"]))
        cur.execute(sql)
        recset = cur.fetchone()
        
        # Notas
        sql2 = str("select n1, n2, n3, n4 from notas where idalunofk = {}".format(id["idAluno"]))
        cur.execute(sql2)
        recset2 = cur.fetchone()

        #parametros
        nome = recset[1]
        n1 = recset2[0]
        n2 = recset2[1]
        n3 = recset2[2]
        n4 = recset2[3]
        media = (n1+n2+n3+n4)/4

        params = [n1, n2, n3, n4, media]

        return render_template('get_notas.html', nome=nome, params=params)
    
    except:
        return render_template('index.html', message="O id do usuário não foi encontrado")


@app.route("/adicionar", methods=['GET', 'POST'])
def adicionar():
    if request.method == "GET":
        return render_template('add_notas.html')
    
    if request.method == "POST":

        id = request.form["idaluno"]
        nome = request.form["nome"]
        n1 = request.form["Nota1"]
        n2 = request.form["Nota2"]
        n3 = request.form["Nota3"]
        n4 = request.form["Nota4"]

        conn.insert(id, nome, n1, n2, n3, n4)
        
        return render_template('add_notas.html', message="Notas Adicionadas Com sucesso")

@app.route("/get_all", methods=["GET"])
def get_all():
    lista = conn.get_all()   
    print(lista)
    return render_template("get_all.html", lista=lista)

@app.route("/atualizar", methods=["POST"])
def atualizar():
    try:
        id = request.form['id']

        con = conn.connection()
        cur = con.cursor()
        
        
        # Alunos
        sql = str("select idAluno, nome from alunos where idAluno = {}".format(id))
        cur.execute(sql)
        recset = cur.fetchone()
            
        # Notas
        sql2 = str("select n1, n2, n3, n4 from notas where idalunofk = {}".format(id))
        cur.execute(sql2)
        recset2 = cur.fetchone()

        #parametros
        nome = recset[1]
        n1 = recset2[0]
        n2 = recset2[1]
        n3 = recset2[2]
        n4 = recset2[3]
        

        params = [id, nome, n1, n2, n3, n4]  

        return render_template("atualizar.html", params=params)
    except:
        return render_template("index.html", message="O id não corresponde a nenhum id existente")


@app.route("/update", methods=["GET","POST"])
def update():
    con = conn.connection()
    cur = con.cursor()
    
    #params
    id = request.form['id']
    nome = request.form['nome']
    n1 = request.form['nota1']
    n2 = request.form['nota2']
    n3 = request.form['nota3']
    n4 = request.form['nota4']

    
    #Alunos
    sql = """Update alunos set nome =  %s where idAluno = %s"""
    cur.execute(sql, (nome, id))
    con.commit()

    #Notas
    sql2 = """Update notas set n1 =  %s, n2 = %s, n3 = %s, n4 = %s where idAlunofk = %s"""
    cur.execute(sql2, (n1, n2, n3, n4, id))
    con.commit()

    return render_template("index.html")
