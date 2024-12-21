from uuid import uuid4

from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask import send_from_directory
from data import db

import main
from markupsafe import Markup, escape
import uuid
import pdf_generator


app = Flask("__name__")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.create_all()



@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login/", methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route("/login/", methods=['GET_POST'])



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






