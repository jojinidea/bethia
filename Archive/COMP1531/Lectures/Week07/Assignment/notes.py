# routes.py is a controller - not all functionality should be put inside routes.py. It really is a controller, intercepts all flask requests
# Categories = {
# x.__name__: x for x in Prouct.__subclasses__()
# key is the name of the class, value is the actual class it's associated with

# }

CATEGORIES = {
    x.__name__: x for x in Product.__subclasses__()

}

CLOTHING = {
    x.__name__: x for x in Clothing.__subclasses()

}

# merge contents in two dictionaries above, extract contents in both, merge, create new dictionary

ALL_ITEMS = {**CLOTHING, **CAMPING}
ALL_ITEMS.keys #returns names of the dictionary - shirt, pants, accessores, miscellaneous
# can pass this to jinja template

#loading data
class OnlineShoppingData:
    @classmethod #means don't have to create any instances of this class
    def load_data(cls):
        warehouse = Warehouse()
        a1 = Accessories("gloves, 10, "S", "Blue)
        
        warehouse.add_item(a1)
        
#routes.py, run.py, server.py

#server.py
#import flask
#import other things that we know, e.g. Warehouse, OnlineShoppingData
#app = Flask(__name__) - a machine needs to have a webserver installed on a computer that understands the language of HTTP.
#flask webserver intercepts request, passes the request to the instance of the flask you've created. app = Flask(__name__)
#start with server.py - imports modules. then we go into routes.py- we need to import that flask instance
#run.py - relies on route imports. We need to import app, warehouse from routes, because the server doesn't contain the routes

#run.py

from routes import app, warehouse

if __name__ == '__main__':
    app.run(debug=TRUE) 
    
    warehouse.save_data() #any new products you've added in will be saved. Persistence
   
#routes.py

#import backend modules we need e.g. from lib.products import ALL_ITEMS, CATEGORIES, CLOTHING, CAMPING

@app.route('/'): #homepage
def home():
    return render_template('home.html') #static html page for home
    
@app.route('/search'):
def search():
    #we want to build a search page
    #GET - gets information, POST - does something with the information 
    #parameters we pass into the form will be visible in the URL 
    #post is when we don't want parameters to be shown in URL, e.g. password etc. 
    #takes form data, stores it in object called request
    if request.args.get('s') if not None: #gives parameters passed in to me through form  
    #need to reference this with exactly the same name I use on the html page as the textbox
        select = request.args.get('select', 'all_btn')
        #whenever I have a get followed by an argument, corresponds to form element on the page
        #gets values passed into that form page
        #tells me what type of search this is
    search_str = request.args.get('s')
    if select == 'cat_btn': 
        category_name = request.args.get('cat')
        results = warehouse.search_cat(category_name, search_str)
    elif select == 'sub_btn':
        sub_category_name = request.arg.get('sub', "") #EMPTY
        results = warehouse.search_subcat(subcategory_name, search_str)
    else: 
        results = warehouse.search_all(search_str)
    return render_template('search.html', results = results, choices = list(CATEGORIES.keys), sub_choices = list(ALL_ITEMS.keys)) #first results is key (in html file), second is value
    #when we pass parameters into the jinja template, we need to specify a key (html) and a value (routes.py)        
      #request object created for me by flask - contains key value pairs of form elements
      #get takes in the form element and returns the value corresponding to the cat
      #doubly curly braces followed by name of the variable you want to print out
      
