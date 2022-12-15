from copy import deepcopy
import json
import requests
import pickle
import csv



"""downlaods cocktail dictionary from http://thecocktaildb.com"""
def get_cocktails():

    iterations = int(input("Enter range of drink IDs to try from 11000: "))

    #create cocktails dictionary
    cocktail_dictionary = {}

    #iterate drink IDs to obtain drinks
    for n in range(iterations):
        
        #query API for reesponse matching drink ID
        #response = requests.get(f"http://www.thecocktaildb.com/api/json/v2/9973533/lookup.php?i={11000 + n}")
        
        response = requests.get(f"http://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={11000 + n}")
        
        data = response.json()
        
        #try all this, in case drink ID invalid and no response receieved
        try:

            #extract drink name and drink id
            strDrink = data['drinks'][0]['strDrink'].title()
            idDrink = data['drinks'][0]['idDrink'].title()
            
            #create cocktail dictionary entry
            cocktail_dictionary.update({strDrink : [idDrink]})
            
            #add drink ingredients
            for i in range(9):
                ingredient = data['drinks'][0][f"{'strIngredient' + str(i + 1)}"]
                if ingredient != None:
                    cocktail_dictionary[strDrink].append(ingredient.title())

            #provide user update on prgress        
            print(f"{11000 + n} {strDrink}")
            

        except TypeError:
            pass
        
        except JSONDecodeError:
            pass

    return cocktail_dictionary


    
"""Returns a dictionary of ingredients with which cocktail name and drink ID in which they are used"""
def build_ingredients_dictionary(ingredients, cocktail_dictionary):
    #declare items dictionary, with ingredients as keys
    items = {}
    for ingredient in range(len(ingredients)):
        items.update({ingredients[ingredient]:[]}) 

    #iterate through coktails dictionary
    for key in cocktail_dictionary:
        #extract each line
        line = cocktail_dictionary.get(key)
        #store drink ID in variable idDrink
        idDrink = cocktail_dictionary[key]["idDrink"]
        #store cocktail constituent ingredients as list in variable constituents
        constituents = list((line.get("ingredients").keys()))
        #iterate through constiuent ingredients
        for i in range(len(constituents)):
            constituent = (constituents[i].title())
            #if constiuent is in the items dictionary add cocktail name and drink ID, or print error message
            if constituent in items:
                items[constituent].append({key:idDrink})
            else:
                print(f"{constiuent} not added to items")
    return items
    


    
