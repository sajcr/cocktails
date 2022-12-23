from flask import Flask, render_template, request
import sqlite3
from cs50 import SQL

db = SQL("sqlite:///cocktails.db")

class Cocktail:
  def __init__(self, drink_id):
  
    db_entry = db.execute("SELECT * FROM cocktails WHERE idDrink = ?", drink_id)[0]
    
    #extract properties from db_entry and assign
    self.id = db_entry['idDrink']
    self.name = db_entry['strDrink']
    self.instructions = db_entry['strInstructions']
    self.glass = db_entry['strGlass']
    self.category = db_entry['strCategory']
    
    #compile list of dictionaries with ingredient and measure, then assign
    ingredients = []
    for n in range(db_entry['numIngredients']):
        item = {
            "ingredient": db_entry[f'strIngredient{n+1}'],
            "measure": db_entry[f'strMeasure{n+1}'],
        }
        ingredients.append(item)
    self.ingredients = ingredients
    
  """ takes list items held, returns number of required ingredients missing """
  def availability(self, items):
    index = len(self.ingredients)
    for ingredient in self.ingredients:
      if ingredient['ingredient'] in items:
        index -= 1
      else:
        pass
    return index
    

class Cabinet:
  def __init__(self):
    
    request_1 = db.execute("SELECT item, category, have FROM ingredients")
    items = {}
    for row in request_1:
      items.update({row['item'] : {'category' : row['category'],'have' : row['have']}})
    
    self.items = items

    request_2 = db.execute("SELECT DISTINCT category FROM ingredients")    
    categories = {}
    for row in request_2:
      categories.update({row['category']:[]})
    for item in items.keys():
      categories[items[item]['category']].append(item)
    
    self.categories = categories

  def have(self):
    have = []
    for entry in self.items:
      if self.items[entry]['have']:
        have.append(entry)
    return have
    
  def lack(self):
    lack = []
    for entry in self.items:
      if not entry['have']:
        lack.append(entry)
    return lack
    
    
       
drink = Cocktail(11000)




cabinet = Cabinet()

print(cabinet.have())



