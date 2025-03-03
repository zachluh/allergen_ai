from dbm import error
from uuid import uuid4

from flask import Flask, render_template, request, url_for, flash, redirect, session, jsonify
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy

import main
from markupsafe import Markup, escape
import uuid
import pdf_generator
import os

from werkzeug.utils import secure_filename

import images


app = Flask("__name__")
app.secret_key = os.getenv("SESSION_KEY")
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



if os.getenv("FLASK_ENV") == "production":
    DATABASE_URL = os.getenv("DATABASE_URL")
else:
    DATABASE_URL = 'sqlite:///app.db'

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

if os.getenv('FLASK_ENV') == 'production':
    app.config['SQLALCHEMY_BINDS'] = {
        'users': DATABASE_URL.replace('/app_db', '/users_db'),
        'recipes': DATABASE_URL.replace('/app_db', '/recipes_db')
    }
else:
    app.config['SQLALCHEMY_BINDS'] = {
        'users': 'sqlite:///users.db',
        'recipes': 'sqlite:///recipes.db'
    }

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
    user = db.Column("user", db.Integer)
    name = db.Column("name", db.String(100))
    true_name = db.Column("true_name", db.String(100))

    def __init__(self, user, name, true_name):
        self.user = user
        self.name = name
        self.true_name = true_name

with app.app_context():
    db.create_all()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/account_page/", methods=["GET", "POST"])
def account_page():
    user = users.query.filter_by(_id=session["user"]).first()
    user_recipes = recipes.query.filter_by(user=session["user"]).all()
    print("ran")
    return render_template('account_page.html', first_name=user.first_name, recipes=user_recipes)

@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        found_user = users.query.filter_by(email=request.form.get('email'), password=request.form.get('password')).first()
        if found_user:
            print("Login success")
            session["user"] = found_user._id
            return redirect(url_for('account_page'))
        else:
            print("Login unsuccessful")
    return render_template('login.html')

@app.route("/signup/", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":

        existing_email = users.query.filter_by(email=request.form.get('email')).first()

        if not existing_email:

            user = users(request.form.get('first_name'), request.form.get('last_name'), request.form.get('email'), request.form.get('password'))

            first_name = request.form.get('first_name')

            db.session.add(user)
            db.session.commit()

            print("User " + first_name + "added successfully")
            print(users.query.all())

            session["user"] = user._id

            return redirect(url_for('account_page'))
        else:
            return render_template('signup.html', error="This email is already in use")

    return render_template('signup.html')




@app.route('/create/', methods=['GET'])
def create():
    return render_template('create.html')

@app.route('/create/', methods=['GET', 'POST'])
def generate_recipe():
    meal = request.form.get('meal')
    recipe = request.form.get('recipe')
    allergies = request.form.get('allergies')

    if recipe == '':
        if request.method == 'POST':
            if 'image' not in request.files:
                return "No file part"
            file = request.files['image']
            if file.filename == '':
                return "No selected file"
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                recipe = images.read(filepath)


    response = ''

    if recipe is None:
       response = main.work_from_nothing(meal, allergies)
    else:
       response = main.work(meal, recipe, allergies)

    pdf_name = "recipe" + str(uuid.uuid4()) + ".pdf"
    pdf_generator.generate(response, pdf_name, f"{allergies}-free {meal}")

    if "user" in session:
        saved_recipe = recipes(session["user"], allergies + " free " + meal, pdf_name)
        db.session.add(saved_recipe)
        db.session.commit()


    return render_template('created_recipe.html', recipe=Markup(response.replace('\n', '<br>')), pdf_name=pdf_name)

@app.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    # Assuming you're using SQLAlchemy to interact with your database
    recipe = recipes.query.get(recipe_id)
    if recipe:
        db.session.delete(recipe)
        db.session.commit()
        os.remove("static/" + recipe.true_name);
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    session.pop("user", None)
    return redirect(url_for('index'))

@app.route('/create/<path:pdf_name>')
def download_pdf(pdf_name):
    return send_from_directory('static', pdf_name, mimetype='application/pdf')


if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))  # Use Railway's PORT if available
    app.run(host="0.0.0.0", port=port)



