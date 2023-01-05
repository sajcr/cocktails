from flask import Flask, render_template, request
import sqlite3
from cs50 import SQL
import json

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
      self.index.update({entry.id : entry})
      
  


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
    
    self.json = json.dumps({"id": self.id,
                            "name":self.name,
                            "ingredients": self.ingredients,
                            "measures": self.measures,
                            "instructions":self.instructions,
                            "glass":self.glass,
                            "category":self.category,})
                  
  
  def __repr__(self):
    return self.name  
  
  """ optionally takes ingredients held returns a tuple with two ingredient lists: ( ( have, have,... ) , ( lack, lack ... ) ) """
  def availability(self, ingredients = []):
  
    availability = []
    #incremenet down the variable for each ingredient that is in the provided list
    
    for ingredient in self.ingredients:
      if ingredient in ingredients:
        pass
      else:
        availability.append(ingredient)
        
    #return the variable as an indication of missing ingredients
    return availability
    

class Cabinet:
  def refresh(self):
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

  def __init__(self):
    self.refresh()    
  
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
      if not self.items[entry]['have']:
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

    



book = Book()

idDrinks = db.execute("SELECT idDrink FROM cocktails")
for idDrink in idDrinks:
  cocktail = Cocktail(idDrink['idDrink'])
  book.add([cocktail])


drinks_cabinet = Cabinet()


@app.route("/drink")
def provide():
    if request.args.get("id"):
        idDrink = int(request.args.get("id"))
        
        drink = book.index[idDrink].json
        return drink

    else:
        return 
    
    


"""the cocktails section of website """
@app.route("/", methods=["GET", "POST"])
def index():
    
    
    #refresh the drinks cabinet to reflect any changes to inventory
    drinks_cabinet.refresh()

    
    #obtain a list of items in the cabinet
    items = drinks_cabinet.have()
    #convert to a list of ingredients
    items = convert_items(items)

   
    #compile a list of cocktails for which we have ingredients, for passing to render_template()    
    cocktails = []
    for entry in book:
        missing = entry.availability(items)
        number_missing = len(missing)
        cocktails.append({"id":entry.id, "name":entry.name, "number_missing":number_missing, "missing":missing})

    
    #if url has requested details return that specific drink
    if request.args.get("idDrink"):
        idDrink = int(request.args.get("idDrink"))
        
        drink = book.index[idDrink]
    else:
        drink = None


    print(cocktails)
    return render_template(
        "cocktails.html", cocktails=cocktails, drink=drink
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
    
    
    #refresh the drinks cabinet to reflect any changes to inventory
    drinks_cabinet.refresh()
    
    """
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
    """
    
    
    return render_template("cabinet.html", drinks_cabinet=drinks_cabinet)
    
    
    
