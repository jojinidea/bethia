from flask import Flask, render_template, request, session, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from User import User

#if user logged in, redirect to main page

app = Flask(__name__)
app.secret_key = 'a Highly secret key' #used to encrypt cookies 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # redirects unlogged in users to login pages

auth_model = Auth_model()
db = {"516": ('saer', '123')}

def get_user(user_id):
    #check database/files
    #create user object based on info in there
    user = db.get(user_id)
    if user != None:
        return User(user_id, user[0])   
    return User(user_id) #return user based on userID

def check_password(user_id, password):
    user = db.get(user_id)
    if user != None:
        return passwd == user[1]
        
    return False

@login_manager.user_loader #need to define this
def load_user(user_id):
    #auth_model.get_user(user_id) #returns user object for username or none if doesn't exist
    return get_user(user_id) #return user class if user id exists. Create an object of type userclass, return it

@app.route('/login', methods = ["POST", "GET"]) #any global stuff should be in SERVER.py, all routes in routes.py
def login():
    if current_user.is_authenticated:
        return redirect(url_for('shopping'))
    #if they've submitted a form, login if valid username & password
    if request.method == "POST": #they have sent in a form, so get username 
        user_id = request.form["user"]
        passwd = request.form["pass"]
        if check_password(user_id, passwd):
            #want to log them in if successful
            userobject = get_user(user_id)
            login_user(userobject)
            #want to redirect them to a home page or something
            return redirect(url_for('shopping')) #string here should be the name of the function, not the route
    return render_template("login.html")

@app.route('/logout', methods=["POST"])
@login_required 
def logout(): #don't need to provide argument
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods = ["POST", "GET"]) #displays shopping cart, adds items to it
@login_required #login required to access this page, we can decorate the function
def shopping():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    items = session.get("items", []) #items is a list obtained from cookie. Browser does not currently have cookies. Tries to find key and if it doesn't, returns NONE. For second optional argument, can list what we want to return if it fails
    if request.method == "POST": #they've filled in form so want to add item to list
        new_item = request.form["item"] #named input item in html so we use item as the name in request.form
        items.append(new_item) #append to session cookie
        session["items"] = items #set cookie to some string that represents the dictionary
    return render_template("shopping.html", shopping_list = items) #set argument to whatever variable we want to pass in. Now can manipulate shopping list items in shopping.html

 

