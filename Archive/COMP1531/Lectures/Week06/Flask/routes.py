from app import app


@app.route("/", methods = ["GET", "POST"]) #refers to home
def index():
    return render_template("form.html")
    # return render_template("index.html", list_numbers=x) #returns a template - need the RENDER_TEMPLATE IMPORT 
    #want pages to be dynamic, to display different content when different users login
    #say we want to pass the list on into the template & print out the list
    #giving index.html x
    
@app.route("/something1", methods = ["GET", "POST"])
def something1():
    if request.method == "POST":
        return "You have logged in"
        #do something, login user
        #otherwise render template as usual
    return "thank you for logging in"
    
@app.route("/something/<number>")
def something(number): #pass in name as a parameter
    return render_template("something.html", number = int(number))
    
    
    
#@app.route("/something/")
#def something():
#    return render_template("something.html")

#routes by default only take get requests, so we have to specify the methods we can take in in the app.routes
