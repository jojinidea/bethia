# if I have an __init__.py file, all files within a directory become a module (we can then import these things) 
# create a file called gitignore, add everything we want to ignore in this format .vscode/* this means we ignore this and we don't add them to git tracking

#in our href, we can do this
#<a href = "{{url_for('subreddit', name=subreddit.name)}}"
## url_for is a flask function


@app.route("/r/<name>?)
def subreddit(name):
    return <h1> "Welcome to " + name </h1>
    
#template inheritance - we can create a base template with static stuff & a dynamic part that other templates inherit
#base.html
# we can get every template to implement everything
# we can create a template with the dynamic part
# {% extends "base.html" %} 
# this means that template inherits everything from base.html
# {% block body %} 
#   <h3> Create a subreddit...x</h3>
#   <form method = "post" action = "/create/form"> #need to specify in the route that it will take the get/post request
#   
# {% endblock %}
# if post request, extract information

# login - want to remain logged in if I change tabs, close down tabs
# this works through cookies - small files smalled on your browser by a website
# by browser sends a cookie to that request
# flask_login is a module that handles setting up/cookie business/persistence
# need to install this pip install flask_login


