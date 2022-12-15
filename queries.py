import pickle
import csv
import cabinet
from copy import deepcopy
from colorama import init, Fore, Back, Style


"""returns dictionary of items and the ingredients they make by refering to categorisation.csv"""


def build_key():
    dictionary = {}
    with open("categorisation.csv", "r", encoding="utf-8-sig") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            dictionary.update({row[2]: []})
    with open("categorisation.csv", "r", encoding="utf-8-sig") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            dictionary[row[2]].append(row[0])
    return dictionary


"""takes items (as stored in Cabinet) and converts them into ingredients (as required by cocktails)"""


def convert(items: list):
    ingredients = []
    # use previously defined build_key fuunction to establish the basis of conversion
    conversion = build_key()
    for item in items:
        if item in conversion:
            ingredients.extend(conversion[item])
    return ingredients


"""translates a cabinet into a list of ingredients"""


def translate(cabinet):
    items = []
    for key in cabinet.inventory:
        if cabinet.inventory[key]:
            items.append(key)
    # use previously defined convert function to perform the conversion
    return convert(items)


"""takes cocktail dictionary, list of ingredients, the assumed ingredients, and int, returns cocktail dictionary where have int number of ingredients missing"""


def find_cocktails(
    cocktail_dictionary: dict, cabinet, assumed_items: list, missing_ingredients: int
):
    # produce actual copy of dictionary and an ingredients list
    temp_dictionary = deepcopy(cocktail_dictionary)
    ingredients = translate(cabinet)
    ingredients.extend(assumed_items)
    # remove from cocktail dictionary any drink where dont have all ingredients
    for key in cocktail_dictionary:
        ingredients_required = cocktail_dictionary[key][1:]
        number_ingredients_required = len(ingredients_required)
        # create a list of the required ingredients that are in the cabinet
        ingredients_have = []
        for i in range(len(ingredients_required)):
            if ingredients_required[i] in ingredients:
                ingredients_have.append(ingredients_required[i])

        # establish how many of the ingredients are in the cabinet
        number_ingredients_have = len(ingredients_have)

        if (
            not number_ingredients_required - number_ingredients_have
            <= missing_ingredients
        ):
            temp_dictionary.pop(key, "not found")
        else:
            ingredients_dont_have = [
                j for j in ingredients_required if j not in ingredients_have
            ]
            # append the items held and those missing
            temp_dictionary[key].append({"have": ingredients_have})
            temp_dictionary[key].append({"dont have": ingredients_dont_have})
    return temp_dictionary


"""takes a list of ingredients, returns a list of the cocktails which can be made"""


def which_cocktails(cocktail_dictionary: dict, ingredients: list):

    # produce actual copy of dictionary
    temp_dictionary = deepcopy(cocktail_dictionary)

    # remove from cocktail dictionary any drink where dont have all ingredients
    for key in cocktail_dictionary:
        ingredients_required = cocktail_dictionary[key][1:]
        for required in ingredients_required:
            required = required.title()
            if required not in ingredients:
                temp_dictionary.pop(key, "not found")

    return temp_dictionary


def print_cocktails(cocktail_dictionary):
    if cocktail_dictionary:
        # xreate a sorted list of dictionary keys to put results in alphabetical order
        drinks = sorted(list(cocktail_dictionary.keys()))
        for drink in drinks:
            data = cocktail_dictionary[drink]
            ingredients = data[1 : len(data) - 2 :]
            cocktail_id = data[0]
            have = data[len(data) - 2].get("have")
            print(f"   {Style.NORMAL + drink.upper()} - (", end="")
            for i in range(len(ingredients) - 1):
                if ingredients[i] in have:
                    print(f"{Style.NORMAL + ingredients[i]}, ", end="")
                else:
                    print(f"{Style.DIM + ingredients[i]}{Style.NORMAL +', '}", end="")
            if ingredients[len(ingredients) - 1] in have:
                print(f"{Style.NORMAL + ingredients[len(ingredients) - 1]}", end="")
            else:
                print(f"{Style.DIM + ingredients[len(ingredients) - 1]}", end="")
            print(
                Style.NORMAL + f") - https://www.thecocktaildb.com/drink/{cocktail_id}"
            )
    else:
        print("  No cocktails")
