# COCKTAILS

### Description:
Cocktails enables the user to maintain a record of cocktail ingredients, and return a list of the drinks the ingredients can be used to make.

##### Usage

The first time it starts the program downloads a list of cocktails from www.thecocktaildb.com, which is saved and subsequently used as the cocktail dictionary.  It also initilaises a drinks cabinet, an object which is used to maintain an inventory of the cocktail ingredients held by the user.

The MAIN MENU allows the user to chose between managing the drinks cabinet, finding cocktails, or exiting the program.

From the DRINKS CABINET submenu the user can:
'add' ingredients to the inventory
'remove' ingredients from the inventory
'list' the items that 'are' in the cabinet, or those that 'aren't'
'clear' the inventory
go 'back'to the main menu

From the COCKTAILS submenu the user can:
list the drinks they 'have' all of the ingredients for
list the drinks where they are missing 'one' ingredient
list the drinks where they are missing 'two' ingredients
list 'all' of the cocktails in the cocktail dictionary
    
When the user choses to exit the program the cocktail dictionary and current state of the drinks cabinet are saved.

##### Program Design

The main program is implemented in the file project.py, which also contains 

*main()* - which implements the menu system, loads the cocktail cabinet and cocktail dictionary, and calls the cocktails queries.

*get_cocktails()* - Downloads cocktail information from www.thecocktaildb.com.  data is returned from the api as a JSON object, the relevant fields are parsed into a cocktail dictionary, which is returned by the function.

*find_cocktails()* - Queries the cocktail dictionary to find which drinks can be made with a given list of ingredients.  The function takes: a cocktail dictionary, a list of ingredients possessed and an int providing the criteria of the number of ingredients required by a cocktail which can be missing from the provided list of ingredients. It returns a cocktail dictionary including only the drinks which meet the criteria.

*print_cocktails()* - Takes a cocktail dictionary and returns a string for printing which presents the drinks, the ingredients each drink requires, and the url for the drink recipie on www.thecocktaildb.com 

The drinks cabinet is a class implemented in cabinet.py, which also includes several functions used to convert the inventory into a list of ingredients as understood by the cocktail dictionary.
# cocktails-wa
