from flask import Flask, request #request enables us to diff between get and post requests
from flask import render_template

app = Flask(__name__)

@app.route("/", methods = "GET", "POST")
def index():
    x = [1,2,3,4] #created a static list
    if request.method == "POST":
        #do something, e.g. login user
        #otherwise, render template normally
    return render_template("index.html", list_numbers=x) #loop through and print out list
    #returns template - located in a directory called templates
    #the template contains html

@app.route("/something/<name>")
def something(name): #pass in name as a parameter 
    return "this is a different route " + name #we can get our page to be dynamically changed depending on the parameter (useful for profile pages)
    # OR
    return render_template("something.html", number = int(number)) #we can use whatever the user passes in
    
#alternatively, we can import routes
# import route
# app.py contains all the app logic 
# from app import app
