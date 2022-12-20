import json
import requests
import pickle
import csv
import pandas
import sqlite3
import re
from cs50 import SQL


"""downloads cocktail information http://thecocktaildb.com returns JSON"""


def get_drink(drink_id):

    # queries the api for drink corresponding to drink id
    response = requests.get(
        f"http://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={11000 + drink_id}"
    )

    data = response.json()

    return data


"""builds and returns raw_cocktails.csv (standard iterations on line 81 = 7842)"""


def get_cocktails():

    with open("cocktails.csv", "w") as file:

        # selects fields to request
        fields = [
            "idDrink",
            "strDrink",
            "strCategory",
            "strIBA",
            "strAlcoholic",
            "strGlass",
            "strIngredient1",
            "strIngredient2",
            "strIngredient3",
            "strIngredient4",
            "strIngredient5",
            "strIngredient6",
            "strIngredient7",
            "strIngredient8",
            "strIngredient9",
            "strIngredient10",
            "strIngredient11",
            "strIngredient12",
            "strIngredient13",
            "strIngredient14",
            "strIngredient15",
            "strMeasure1",
            "strMeasure2",
            "strMeasure3",
            "strMeasure4",
            "strMeasure5",
            "strMeasure6",
            "strMeasure7",
            "strMeasure8",
            "strMeasure9",
            "strMeasure10",
            "strMeasure11",
            "strMeasure12",
            "strMeasure13",
            "strMeasure14",
            "strMeasure15",
        ]

        # writes header row to csv with chosen fields
        for m in range(len(fields) - 1):

            file.write(f"{fields[m]},")

        file.write(f"strMeasure15\n")
        # file.write(f"\n")

        # iterate through drink ids submitting each as a request for data
        for n in range(7842):

            # print number of request to stout to indicate progress
            print(n, end="")

            # try this each time as some drink ids return nothing
            try:

                # submit request and save response data fields within temporary variable cocktail
                cocktail = get_drink(n)["drinks"][0]

                # print cocktail name to stout, to accompany drink id and give indication of success
                print(f" - {cocktail['strDrink']}")

                # variable to use when avoiding printing the last comma
                m = len(fields)

                # iterate through fields and write each to csv
                for field in fields:

                    m = m - 1

                    # extract actual cocktail entry
                    entry = cocktail[field]

                    # if there is data then cast to title case to ensure consistency
                    if entry:
                        entry = entry.title()

                    # do not add any cocktail using list of unwanted ingredients
                    if entry in [
                        "Cider",
                        "Apple Cider",
                        "Coconut Milk",
                        "Hot Chocolate",
                        "Absolut Citron",
                        "Lemon Vodka",
                        "Guinness Stout",
                        "Melon Liqueur",
                        "Blackcurrant Squash",
                        "Blueberry Schnapps",
                        "Peychaud Bitters",
                        "Raspberry Vodka",
                        "Wormwood",
                        "Fruit Juice",
                        "Passoa",
                        "Coconut Liqueur",
                        "Peach Brandy",
                        "Cream Of Coconut",
                        "Applejack",
                        "151 Proof Rum",
                        "Zima",
                        "Dr. Pepper",
                        "Maui",
                        "Sarsaparilla",
                        "Chocolate Syrup",
                        "Blackberry Brandy",
                        "Grape Juice",
                        "Root Beer",
                        "Half-And-Half",
                        "Lager",
                        "Carrot",
                        "Asafoetida",
                        "Goldschlager",
                        "Jello",
                        "Coconut Rum",
                        "Limeade",
                        "St. Germain",
                        "Pineapple Syrup",
                        "Dubonnet Rouge",
                        "Erin Cream",
                        "Mountain Dew",
                        "Everclear",
                        "Vanilla Vodka",
                        "Pepsi Cola",
                        "Fresca",
                        "Chocolate Milk",
                        "Pisang Ambon",
                        "Peach Bitters",
                        "Papaya",
                        "Crown Royal",
                        "Glycerine",
                        "Coffee Brandy",
                        "Vermouth",
                        "Lillet",
                        "Falernum",
                        "Sweet And Sour",
                        "Peach Vodka",
                        "None",
                        "Salted Chocolate",
                        "Lime Vodka",
                        "Cantaloupe",
                        "Tropicana",
                        "Bacardi Limon",
                        "Oreo Cookie",
                        "Blackstrap Rum",
                        "Firewater",
                        "Dark Creme De Cacao",
                        "Grape Soda",
                        "Carbonated Soft Drink",
                        "Strawberry Schnapps",
                        "Lemon-Lime Soda",
                        "Pina Colada Mix",
                        "Sour Mix",
                        "Fruit",
                        "Cornstarch",
                        "Tennessee Whiskey",
                        "Hot Damn",
                        "Agave Syrup",
                        "Marjoram Leaves",
                        "Fruit Punch",
                        "Kool-Aid",
                        "Absolut Peppar",
                        "Cranberries",
                        "Chocolate Sauce",
                        "Iced Tea",
                        "Mango",
                        "Cherries",
                        "Raspberry Liqueur",
                        "Peppermint Schnapps",
                        "Absolut Kurant",
                        "Coconut Syrup",
                        "Surge",
                        "Pisco",
                        "Orange Spiral",
                        "Cherry Grenadine",
                        "Peppermint Extract",
                        "Vanilla Ice-Cream",
                        "Ale",
                        "Peach Nectar",
                        "Strawberry Liqueur",
                        "Sherbet",
                        "Orgeat Syrup",
                        "Apfelkorn",
                        "Cherry Heering",
                        "Chocolate",
                        "Berries",
                        "Elderflower Cordial",
                        "Gold Rum",
                        "Sirup Of Roses",
                        "Gold Tequila",
                        "Godiva Liqueur",
                        "None",
                        "Almond",
                        "Beer",
                        "Grain Alcohol",
                        "Corona",
                        "Raspberry Syrup",
                        "Maple Syrup",
                        "Orange Curacao",
                        "Añejo Rum",
                        "Chocolate Liqueur",
                        "Lillet Blanc",
                        "Black Pepper",
                        "Guava Juice",
                        "Kiwi Liqueur",
                        "Banana Liqueur",
                        "Corn Syrup",
                        "Pink Lemonade",
                        "Candy",
                        "Black Sambuca",
                        "Marshmallows",
                        "Mint Syrup",
                        "Kirschwasser",
                        "Frangelico",
                        "Apple Schnapps",
                        "Peachtree Schnapps",
                        "Honey Syrup",
                        "Blackberries",
                        "Condensed Milk",
                        "Creme De Banane",
                        "Kummel",
                        "Daiquiri Mix",
                        "Aquavit",
                        "Butterscotch Schnapps",
                        "Chocolate Ice-Cream",
                        "Grapes",
                        "Jagermeister",
                        "Vanilla",
                        "Angelica Root",
                        "Schweppes Russchian",
                        "Rumple Minze",
                        "Maraschino Liqueur",
                        "Almond Flavoring",
                        "Passion Fruit Syrup",
                        "Apricot",
                        "Midori Melon Liqueur",
                        "Yellow Chartreuse",
                        "Cranberry Vodka",
                        "Yukon Jack",
                        "Olive Brine",
                        "Food Coloring",
                        "Lavender",
                        "Caramel Coloring",
                        "Licorice Root",
                    ]:
                        print("flag!")
                        break

                    file.write(f"{entry}")

                    # print a comma following all but last entry
                    if m > 0:
                        file.write(f",")

                file.write(f"\n")

            except:
                print(" ")
                pass


""" writes from cocktails.csv to cocktails.db """


def write_cocktails():

    # establish connection with database
    conn = sqlite3.connect("../cocktails.db")

    # initiate table
    conn.execute(
        "CREATE TABLE if not exists cocktails (idDrink INT PRIMARY KEY,strDrink,strCategory,strIBA,strAlcoholic,strGlass,strIngredient1,strIngredient2,strIngredient3,strIngredient4,strIngredient5,strIngredient6,strIngredient7,strIngredient8,strIngredient9,strIngredient10,strIngredient11,strIngredient12,strIngredient13,strIngredient14,strIngredient15,strMeasure1,strMeasure2,strMeasure3,strMeasure4,strMeasure5,strMeasure6,strMeasure7,strMeasure8,strMeasure9,strMeasure10,strMeasure11,strMeasure12,strMeasure13,strMeasure14,strMeasure15,strInstructions,numIngredients)"
    )

    # write data
    df = pandas.read_csv("cocktails.csv")
    df.to_sql("cocktails", conn, if_exists="append", index=False)


"""returns a list of all ingredients listed in cocktails.db which are undefined in ingredients.csv"""


def check_ingredients():

    # establish database connection
    conn = sqlite3.connect("../cocktails.db")
    # get all ingredients in db
    data = conn.execute(
        "SELECT strIngredient1,strIngredient2,strIngredient3,strIngredient4,strIngredient5,strIngredient6,strIngredient7,strIngredient8,strIngredient9,strIngredient10,strIngredient11,strIngredient12,strIngredient13,strIngredient14,strIngredient15 FROM cocktails;"
    )

    # initiate empty set to hold unique ingredients
    ingredients = set()

    # add each ingredient to the set (trying in case the value is none)
    for row in data:
        for item in row:
            try:
                ingredients.add(item)
            except:
                pass

    # cast dbingredients back to a list
    ingredients = list(ingredients)

    # get the contents of the ingredients csv file
    with open("ingredients.csv", "r") as file:
        contents = file.read()

    # use regx to comile a list of ingredients that are defined in ingredients.csv
    entries = re.findall("\\n.*,", contents)
    counter = 0
    for entry in entries:
        entry = entry.split("\n", 1)[1]
        entry = entry.split(",", 1)[0]
        entries[counter] = entry
        counter += 1

    # remove all defined ingredients from the dbingredients list
    for entry in entries:
        try:
            ingredients.remove(entry)
        except:
            pass

    # remove any 'none' ingredients
    ingredients.remove("None")

    # return list of undefined inredients
    print(
        f"The following ingredients in the cocktails list remain unaccounted for: {ingredients}"
    )


""" writes ingredients.csv to cocktails.db """


def write_ingredients():
    # establish connection with database
    conn = sqlite3.connect("../cocktails.db")

    # initiate table
    conn.execute(
        "CREATE TABLE if not exists ingredients (ingredient TEXT PRIMARY KEY, item TEXT DEFAULT null, category TEXT Default null, have NUMERIC DEFAULT 0)"
    )
    # write data
    df = pandas.read_csv("ingredients.csv")
    df.to_sql("ingredients", conn, if_exists="append", index=False)
    

def add_recipies():
  db = SQL("sqlite:///../cocktails.db")

  # initiate table
  drink_ids = db.execute("SELECT idDrink FROM cocktails") 
  
  for drink_id in drink_ids:
    
    #amend drink id for use wuth get_drink() and request data from cocktaildb
    request = drink_id['idDrink'] - 11000
    cocktail = get_drink(request)
    
    #extract instructions from request
    strInstructions = (cocktail['drinks'][0]['strInstructions'])
    
    #update database with instructions
    db.execute("UPDATE cocktails SET strInstructions = ? WHERE idDrink = ?", strInstructions, drink_id['idDrink'])



def add_number_ingredients():
  db = SQL("sqlite:///../cocktails.db")
  
  #get relevant data from db
  drinks = db.execute("SELECT idDrink,strIngredient1,strIngredient2,strIngredient3,strIngredient4,strIngredient5,strIngredient6,strIngredient7,strIngredient8,strIngredient9,strIngredient10,strIngredient11,strIngredient12,strIngredient13,strIngredient14,strIngredient15 FROM cocktails") 
  
  #for each drink count the number of ingredients
  for drink in drinks:
    
    count = 0
    for n in range(15):
      ingredient = drink[f"strIngredient{n+1}"]
      
      if ingredient == "None":
        pass
      else:
        count += 1
    
    #add the ingredients number into the db
    db.execute("UPDATE cocktails SET numIngredients = ? WHERE idDrink = ?", count, drink['idDrink']) 
    print(f"{drink['idDrink']} - {count}")
        
      
    
  

    
def main():
    while True:
        print(
            "\n1. Get cocktails.csv \n2. Write cocktails to database \n3. Check ingredients \n4. Write ingredients to database\n5. Add recipies to database\n6. Add number of ingredients to database"
        )
        choice = input("Enter 1, 2, 3, 4, 5 or 6: ")
        if choice == "1":
            get_cocktails()
            print("\n Don't forget to clean up cocktails.csv before proceeding")
        elif choice == "2":
            write_cocktails()
        elif choice == "3":
            check_ingredients()
        elif choice == "4":
            write_ingredients()
        elif choice == "5":
            add_recipies()
        elif choice == "6":
          add_number_ingredients()
        else:
            pass


if __name__ == "__main__":
    main()
