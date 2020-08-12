from flask import Flask, render_template, request, redirect, url_for

# to create our app, we need to create an instance of it

app = Flask(__name__)

# define all routes in routes.py

#/index.html to give back specific content 

app.run(port=555, debug = True) #specify a port number to visit the website, error output will display on the webpage

#to visit /localhost.555/index.html

#associates route with function below it

@app.route("/index.html", methods = ["GET", "POST"]) #I want http:///localhost.555/index.html to return some content
def index():
    # return '<h1> Hello, World! </h1>' instead of this, we can use render_template
    # only concerned with 
    #1 request.method and 
    #2 request.form
    if request.method == "POST": #handle post requests differently to get requests
        #indicates the user must have sent that form
        #by default, all routes are configured to handle a "GET" request - need to specify the route should handle GET & POST requests
        return render_template("response.html", name = request.form['name'], iq = request.form['iq'])
        #jinja2 - any file you give to render_template is tampered with my jinja2
        #return "This guy %s has %s IQ" %(request.form['name'], request.form['iq'])
        #print(request.form)

@app.route("/<name>/<age>") #url completely arbitrary - want to give back personalised content for each of these pages
def nameage(name, age):
    return "this person is named %s with age %s" %(name, age)
    
    return render_template("index.html") #by default looks in the same directory you're on inside a templates directory
    
# must have a function that returns content for a route
# dynamic content requires interaction between the user & the backend
# get requests paste that information in the URL
# post requests sends this in the body that it sends (as opposed to the URL - not visible to us)

#**VALUES ARE all strings**
