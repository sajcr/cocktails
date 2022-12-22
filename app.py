from flask import Flask, render_template, request
import sqlite3
from cs50 import SQL

app = Flask(__name__)


db = SQL("sqlite:///cocktails.db")


@app.route("/", methods=["GET", "POST"])
def index():

    #build a list of items we have in cabinet
    things = db.execute("SELECT ingredient FROM ingredients WHERE have = 1")

    items = []    
    for thing in things:
      items.append(thing['ingredient']) 
      
    print(items)

    #get cocktails details
    entries = db.execute(
        "SELECT idDrink, strDrink, strIngredient1, strIngredient2, strIngredient3, strIngredient4, strIngredient5, strIngredient6, strIngredient7, strIngredient8, strIngredient9, strIngredient10, strIngredient11, strIngredient12, strIngredient13, strIngredient14, strIngredient15 FROM cocktails"
    )
    
    cocktails = []
    
    for entry in entries:
      add = True
      for n in range(15):
        
        if entry[f"strIngredient{n+1}"] in items:
          pass
        elif entry[f"strIngredient{n+1}"] == "None":
          pass
        else:
          add = False
      
      if add == True:
        cocktails.append(entry)
    
    print(cocktails)
    
    if request.args.get("idDrink"):
        idDrink = request.args.get("idDrink")

        drink = db.execute("SELECT * FROM cocktails WHERE idDrink = ?", idDrink)[0]

    else:

        drink = db.execute("SELECT * FROM cocktails")[0]

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


@app.route("/cabinet", methods=["GET", "POST"])
def cabinet():

    if request.method == "POST":

        haves = request.form.getlist("check")

        db.execute("UPDATE ingredients SET have = 0")

        for have in haves:
            db.execute("UPDATE ingredients SET have = 1 WHERE item = ?", have)

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
