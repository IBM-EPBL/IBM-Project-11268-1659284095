from flask import Flask,render_template,request
import ibm_db

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30426;PROTOCOL=TCPIP;UID=LDM84139;PWD=FAgl73hor4nyJk6r;Security=SSL;SSLSecurityCertificate=DigiCertGlobalRootCA.crt", "", "")
print("Connnected DB")

app = Flask(__name__)

@app.route("/",methods=['GET', 'POST'])
@app.route("/register",methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        name = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        rollno = request.form["rollno"]
        print(name,email,password,rollno)
        insert_sql = "INSERT INTO  LDM84139.USER VALUES (?, ?, ?, ?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, name)
        ibm_db.bind_param(prep_stmt, 2, password)
        ibm_db.bind_param(prep_stmt, 3, email)
        ibm_db.bind_param(prep_stmt, 4, rollno)
        ibm_db.execute(prep_stmt)
        return render_template('login.html', msg = msg) 
    else:
        return render_template('register.html', msg = msg)

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        name = request.form["username"]
        password = request.form["password"]
        select_sql = "SELECT * FROM  LDM84139.USER WHERE USERNAME = ? AND PASSWORD = ?"
        prep_stmt = ibm_db.prepare(conn, select_sql)
        ibm_db.bind_param(prep_stmt, 1, name)
        ibm_db.bind_param(prep_stmt, 2, password)
        out = ibm_db.execute(prep_stmt)
        result_dict = ibm_db.fetch_assoc(prep_stmt)
        print(result_dict)
        if result_dict != False:
            return render_template('welcome.html',msg = msg)
        return render_template('login.html', msg = msg)

    else:
        return render_template('login.html', msg = msg)

@app.route('/welcome', methods =['GET', 'POST'])
def welcome():
    msg = ''
    return render_template('welcome.html', msg = msg)