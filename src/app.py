from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

from src.model.expense import Expense, ExpenseSchema
from src.model.income import Income, IncomeSchema
from src.model.transaction_type import TransactionType    
from src.db_functions import get_db_settings

app = Flask(__name__)

transactions = []

# Initialize flask-sqlalchemy extension
db = SQLAlchemy()
db_settings = get_db_settings()
db_uri =db_settings[0]
db_secretkey = db_settings[1]

# Tells flask-sqlalchemy what database to connect to
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SECRET_KEY"] = db_secretkey

# LoginManager is needed for our application
# to be able to log in and out users
login_manager = LoginManager()
login_manager.init_app(app)
 
# Initialize app with extension
db.init_app(app)

# Create user model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True,
                         nullable=False)
    password = db.Column(db.String(250),
                         nullable=False)
    def __repr__(self):
        return f"<User usermame:{self.username} password:{self.password}"
 

# Create database within app contex
with app.app_context():
    db.create_all()

# Creates a user loader callback that returns the user object given an id
@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)

### Route setup ###
@app.route("/")
def home():
    # Render home.html on "/" route
    return render_template("home.html")

@app.route('/register', methods=["GET", "POST"])
def register():
  # If the user made a POST request, create a new user
    if request.method == "POST":
        user = User(username=request.form.get("username"),
                     password=request.form.get("password"))
        # Add the user to the database
        db.session.add(user)
        # Commit the changes made
        db.session.commit()
        # Once user account created, redirect them
        # to login route (created later on)
        return redirect(url_for("login"))
    # Renders sign_up template if user made a GET request
    return render_template("sign_up.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    # If a post request was made, find the user by
    # filtering for the username
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form.get("username")).first()
        # Check if the password entered is the
        # same as the user's password
        if user.password == request.form.get("password"):
            # Use the login_user method to log in the user
            login_user(user)
            print("sucess")
            return redirect(url_for("home"))
        # Redirect the user back to the home
        # (we'll create the home route in a moment)
    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/incomes")
def get_incomes():
    
    # schema will contain many objects
    schema = IncomeSchema(many=True)
    
    # Used lambda to filter out any NON incomes
    incomes = schema.dump(
        filter(lambda t: t.type == TransactionType.INCOME, transactions)
    )

    return jsonify(incomes)

@app.route("/incomes", methods=['POST'])
@login_required
def add_income():
    income = IncomeSchema().load(request.get_json())
    transactions.append(income)
    # Return message and statuscode
    return "", 204

@app.route("/expenses")
@login_required
def get_expenses():
    schema = ExpenseSchema(many=True)
    expenses = schema.dump(
        filter(lambda t: t.type == TransactionType.EXPENSE, transactions)
    )

    return jsonify(expenses)

@app.route("/expenses", methods=['POST'])
def add_expense():
    expense = ExpenseSchema().load(request.get_json())
    transactions.append(expense)
    return "", 204

