from flask import Flask, render_template, request
import sqlite3
from cs50 import SQL

"""Be aware fo the difference between ingredients (as understood by the cocktail recipies),
and items (as understood by the cabinet)"""



app = Flask(__name__)


db = SQL("sqlite:///data/cocktails.db")


class Book:
  def __init__(self):
    #a list of the names of all entries
    self.contents = []
    #an index of entry.id : entry
    self.index = {}
  
  #make iterable accross the index of cocktails  
  def __iter__(self):
    for entry in self.index:
      yield self.index[entry]
  
  #enables addition of cocktails     
  def add(self, entries):
    for entry in entries:
      self.contents.append(entry.name)
      self.index.update({entry.id:entry})
      
  


""" will want to define a p[arent class and redfine this as a child, eventually """
class Cocktail:
  def __init__(self, drink_id):
    
    #query cocktail table in database
    db_entry = db.execute("SELECT * FROM cocktails WHERE idDrink = ?", drink_id)[0]
    
    #extract properties from db_entry and assign
    self.id = db_entry['idDrink']
    self.name = db_entry['strDrink']
    self.instructions = db_entry['strInstructions']
    self.glass = db_entry['strGlass']
    self.category = db_entry['strCategory']
    
    #compile list of dictionaries with ingredient and measure, then assign
    ingredients = []
    measures = []
    for n in range(db_entry['numIngredients']):
        ingredients.append(db_entry[f'strIngredient{n+1}'])
        measures.append(db_entry[f'strMeasure{n+1}'])
    self.ingredients = tuple(ingredients)
    self.measures = tuple(measures)
  
  def __repr__(self):
    return self.name  
  
  """ optionally takes ingredients held returns a tuple with two ingredient lists: ( ( have, have,... ) , ( lack, lack ... ) ) """
  def availability(self, ingredients = []):
  
    availability = ([],[])
    #incremenet down the variable for each ingredient that is in the provided list
    
    for ingredient in self.ingredients:
      if ingredient in ingredients:
        availability[0].append(ingredient)
      else:
        availability[1].append(ingredient)
        
    #return the variable as an indication of missing ingredients
    return availability
    

class Cabinet:
  def __init__(self):
    """ state of cabinet as a dictionary of format - { item : { 'category' : category, 'have' : have } , .. } """
    request_1 = db.execute("SELECT item, category, have FROM ingredients")
    items = {}
    for row in request_1:
      items.update({row['item'] : {'category' : row['category'],'have' : row['have']}})
    self.items = items
    
    """ categorisation of items as a dictionary of format { category : [ item, item, item ...] , .. } """
    request_2 = db.execute("SELECT DISTINCT category FROM ingredients")    
    categories = {}
    for row in request_2:
      categories.update({row['category']:[]})
    for item in items.keys():
      categories[items[item]['category']].append(item)
    self.categories = categories
  
  """ returns a list of items held """
  def have(self):
    have = []
    for entry in self.items:
      if self.items[entry]['have']:
        have.append(entry)
    return have
  
  """ returns a list of items not held """  
  def lack(self):
    lack = []
    for entry in self.items:
      if not entry['have']:
        lack.append(entry)
    return lack


""" takes an ingredient, or list of ingredients, returns as a set of items """
def convert_ingredients(ingredients):
  # if received a single ingredient as a str, change this for a list with single ingredient duplicated
  if type(ingredients) == str:
    ingredients = list([ingredients, ingredients])
  items = set()
  #look up each ingredient in db and obtain corresponding item
  for ingredient in ingredients:
    db_entry = db.execute("SELECT item FROM ingredients WHERE ingredient = ?", ingredient)
    items.add(db_entry[0]['item'])
  return(items)
  
  
""" takes an item, or list of items, returns as a set of ingredients """
def convert_items(items):
    # if received a single item as a str, change this for a list with single item duplicated
  if type(items) != list:
    items = list([items, items])
  ingredients = set()
  #look up each item in db and obtain corresponding ingredient
  for item in items:
    db_entry = db.execute("SELECT ingredient FROM ingredients WHERE item = ?", item)
    for field in db_entry:
      ingredients.add(field['ingredient'])
  return(ingredients)

    







"""the cocktails section of website """
@app.route("/", methods=["GET", "POST"])
def index():
    #iinitialise the cabinet.  Could this be outside of the function as a global variable?
    cabinet = Cabinet()
    #obtain a list of items in the cabinet
    items = cabinet.have()
    #create a list of ingredients
    items = convert_items(items)

    #query database for cocktails details
    entries = db.execute(
        "SELECT idDrink, strDrink, strIngredient1, strIngredient2, strIngredient3, strIngredient4, strIngredient5, strIngredient6, strIngredient7, strIngredient8, strIngredient9, strIngredient10, strIngredient11, strIngredient12, strIngredient13, strIngredient14, strIngredient15 FROM cocktails"
    )
    
    #compile a list of cocktails, adding only if all ingredients are included int he items list
    #NOTE: this conflates items and ingredients!
    
    cocktails = []
    for entry in entries:
      #assume that the entry will be added
      add = True
      for n in range(15):
        #refute assumption if any of the ingredient fields are not in the items list, or are not none
        if entry[f"strIngredient{n+1}"] in items:
          pass
        elif entry[f"strIngredient{n+1}"] == "None":
          pass
        else:
          add = False  
      if add == True:
        cocktails.append(entry)
    print(len(cocktails))
    
    #if url has requested details on drink by including drink id get those details only
    if request.args.get("idDrink"):
        idDrink = request.args.get("idDrink")
        drink = db.execute("SELECT * FROM cocktails WHERE idDrink = ?", idDrink)[0]
    #THIS else is WRONG at the moment it is getting all drink details, returnign only that of the 
    #first entry (via the [0])  could it just be pass?  or should it details to make a holding page?""" 
    else:
        drink = db.execute("SELECT * FROM cocktails")[0]
        
    #compile a list of the ingredients and measures to pass to render template
    ingredients = []
    for n in range(drink["numIngredients"]):
        item = {
            "ingredient": drink[f"strIngredient{n+1}"],
            "measure": drink[f"strMeasure{n+1}"],
        }
        ingredients.append(item)
    
    return render_template(
        "cocktails.html", cocktails=cocktails, drink=drink, ingredients=ingredients
    )


""" the cabinet section of website """
@app.route("/cabinet", methods=["GET", "POST"])
def cabinet():
    
    #when receive notification that update button has cliskced get list of checked items..
    if request.method == "POST":
        haves = request.form.getlist("check")
        # reset the items db so all are lacks
        db.execute("UPDATE ingredients SET have = 0")
        # iterate thorugh and 'have' those that are checked
        for have in haves:
            db.execute("UPDATE ingredients SET have = 1 WHERE item = ?", have)
    
    #compile the details required to create the checkbox list
    #This can probably be amended to use the cabinet class functionallity
    items = db.execute(
        "SELECT DISTINCT item, category, have FROM ingredients ORDER BY item"
    )

    entries = []
    # declare categories set to obtain unique values
    categories = []
    for item in items:

        entry = item["item"]
        category = item["category"]

        if item["have"]:
            status = "checked"
        else:
            status = "unchecked"

        entries.append({"item": entry, "category": category, "status": status})

        # add category to set
        categories.append(category)

    # convert categories set back to an ordered list
    categories = set(categories)
    list(categories).sort()

    return render_template("cabinet.html", entries=entries, categories=categories)
    
    
    
