#up to 36 min in the lecture
#second route not working for some reason - the one with numbers
from flask import Flask, render_template
# need to import Flask from our flask module

app = Flask(__name__) 

import routes



# how do websites work
# when I type in a website (e.g. www.google.com), my browser is communicating to google.com (I send a request to google.com, google.com gets my request and gives html back to me) 

# what I get back depends on the route, or the url I put in
