from flask import Flask, render_template, request, url_for, flash, redirect
import main
import sys
from markupsafe import Markup, escape
from reportlab.pdfgen.canvas import Canvas


app = Flask("__name__")

pdf = Canvas("recipe.pdf")



@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login/", methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/create/', methods=['GET'])
def create():
    return render_template('create.html')

@app.route('/create/', methods=['GET', 'POST'])
def generate_recipe():
    meal = request.form.get('meal')
    recipe = request.form.get('recipe')
    allergies = request.form.get('allergies')

    response = ''

    if (recipe is None):
       response = main.work_from_nothing(meal, allergies)
    else:
       response = main.work(meal, recipe, allergies)

    return render_template('created_recipe.html', recipe=Markup(response.replace('\n', '<br>')))






