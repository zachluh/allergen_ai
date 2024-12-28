from uuid import uuid4

from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer

import main
from markupsafe import Markup, escape
import uuid
import pdf_generator


app = Flask("__name__")
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

app.config['SQLALCHEMY_BINDS'] = {
        'users': 'sqlite:///users.db',
        'recipes': 'sqlite:///recipes.db'
    }

db = SQLAlchemy(app)

class users(db.Model):

    __bind_key__ = 'users'
    __tablename__ = 'users_table'

    _id = db.Column("id", db.Integer, primary_key=True)
    first_name = db.Column("first_name", db.String(100))
    last_name = db.Column("last_name", db.String(100))
    email = db.Column("email", db.String(100))
    password = db.Column("password", db.String(100))


    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password


class recipes(db.Model):
    __bind_key__ = 'recipes'
    __tablename__ = 'recipes_table'

    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))

    def __init__(self, name):
        self.name = name

with app.app_context():
    db.create_all()



@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        found_user = users.query.filter_by(email=request.form.get('email'), password=request.form.get('password')).first()
        if found_user:
            print("Login success")
            return render_template('account_page.html', first_name=found_user.first_name)
        else:
            print("Login unsuccessful")
    return render_template('login.html')

@app.route("/signup/", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":

        user = users(request.form.get('first_name'), request.form.get('last_name'), request.form.get('email'), request.form.get('password'))

        first_name = request.form.get('first_name')

        db.session.add(user)
        db.session.commit()

        print("User " + first_name + "added successfully")
        print(users.query.all())

        return render_template('account_page.html', first_name=first_name)
    return render_template('signup.html')




@app.route('/create/', methods=['GET'])
def create():
    return render_template('create.html')

@app.route('/create/', methods=['GET', 'POST'])
def generate_recipe():
    meal = request.form.get('meal')
    recipe = request.form.get('recipe')
    allergies = request.form.get('allergies')

    response = ''

    if recipe is None:
       response = main.work_from_nothing(meal, allergies)
    else:
       response = main.work(meal, recipe, allergies)

    pdf_name = "recipe" + str(uuid.uuid4()) + ".pdf"
    pdf_generator.generate(response, pdf_name)

    return render_template('created_recipe.html', recipe=Markup(response.replace('\n', '<br>')), pdf_name=pdf_name)

@app.route('/create/<path:pdf_name>')
def download_pdf(pdf_name):
    return send_from_directory('static', pdf_name, mimetype='application/pdf')






