
from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)
app.secret_key = 'super-secret-key'
if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

class Query(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_no = db.Column(db.String(12), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    query = db.Column(db.String(120), nullable=False)

class patientd(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.String(80), nullable=False)
    vaccine = db.Column(db.String(80), nullable=False)
    aadhar_no = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    phone_no = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=True)
    gender = db.Column(db.String(80), nullable=False)


@app.route("/")
def homepg():
    return render_template('index.html')

@app.route("/slhomepg", methods=['GET', 'POST'])
def slhomepg():


        return render_template('slhomepg.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/patientlist")
def patientlist():

    return render_template('plist.html', params=params)


@app.route("/currentcovid")
def currentcovid():

    return render_template('currentcovid.html')


@app.route("/stafflogin")
def stafflogin():

    if ('user' in session and session['user'] ==  params['admin_user']):
        return render_template('slhomepg.html', params=params)

    if request.method == 'POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        if (username == params['admin_user'] and userpass == params['admin_password']):
            session['user'] = username
            return render_template('slhomepg.html', params=params)
    else:
        return render_template('stafflogin.html', params=params)

@app.route("/availstaff")
def availstaff():
    return render_template('availstaff.html')

@app.route("/centerdetails")
def centerdetails():
    return render_template('centerdetails.html')

@app.route("/patient", methods = ['GET', 'POST'])
def patient():
    if(request.method=='POST'):
        name = request.form.get('name')
        age = request.form.get('age')
        vaccine = request.form.get('vaccine')
        aadhar_no = request.form.get('aadhar_no')
        phone_no = request.form.get('phone_no')
        address = request.form.get('address')
        gender = request.form.get('gender')
        entry = patientd(name=name, age=age, vaccine=vaccine, aadhar_no=aadhar_no, address=address, gender=gender, date=datetime.now(), phone_no=phone_no, query=query)
        db.session.add(entry)
        db.session.commit()
    return render_template('patient.html')

@app.route("/query", methods = ['GET', 'POST'])
def query():
    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        query = request.form.get('query')
        entry = Query(name=name, email=email, phone_no=phone, date=datetime.now() , query=query)
        db.session.add(entry)
        db.session.commit()
    return render_template('query.html')


@app.route("/homeremedies")
def homeremedies():
    return render_template('homeremedies.html')

app.run(debug=True)