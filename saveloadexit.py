import pickle


"""load assumed ingredients"""
def load_assumed():
    with open("assumed.pkl", "rb") as file:
        return pickle.load(file)


"""save assumed ingredients"""
def save_assumed(assumed: list):
    with open("assumed.pkl", "wb") as file:
        pickle.dump(assumed, file)


"""saves cocktail dictionary"""
def save_cocktails(cocktail_dictionary):
    with open("cocktail_dictionary.pkl", "wb") as file:
        pickle.dump(cocktail_dictionary, file)


"""load cocktail dictionary"""
def load_cocktails():
    try:
        with open("cocktail_dictionary.pkl", "rb") as file:
            cocktail_dictionary = pickle.load(file)
        return cocktail_dictionary
    except:
        cocktail_dictionary = {}
        save_cocktails(cocktail_dictionary)
        return cocktail_dictionary


"""exit the programme, saving state"""
def exit():
    drinks_cabinet.save()
    save_assumed(assumed)
    os.system("clear")
    sys.exit()
