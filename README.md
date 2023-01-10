# COCKTAILS
#### Video Demo:  <URL HERE>
#### Description:
Cocktails is a flask webapp which enables the user to store a list of the cocktail ingredients they have, and to see which cocktails they can make from combinatiosn fo those ingredients.

#### Files:
The project includes the following files:

- *./app.py* - the main flask project file containing python code which queries the saved cocktail database (see ./data/cocktails.db below) for information on drinks and ingredients.  The code defines several classes which are then used to process the information and pass relevent data to the html templates.
- *./requirements.txt* - standard flask framework file listing the required libraries

- *./static/styles.css* - standard flask css file, essentially unused as the project makes extensive use of bootstrap
- *./static/martini.svg* - picture used on homepage

- *./templates/cabinet.html* - html for the cabinet section of the webapp (extends layout.html)
- *./templates/cocktails.html* - html for the cocktails section of the webapp (extends layout.html)
- *./templates/layout.html* - base html

- *./data/build_database.py* - a set of helper functions to assist with building (or rebuilding) the cocktail database.  When run in a terminal it provides 7 numbered options which, if chosen sequentially will use the two csv helper files to compile *./data/cocktails.db*
- *./data/cocktails.csv* - a file created by option 1 of *./data/build_database.py* which itemises the cocktail information downloaded from thecocktaildb.com.  Optionally, the file can be manually reviewed before continuing to build the local database.
- *./data/cocktails.db* - a sqllite3 database, used to hold cocktail and ingredient data.  Created (or recreated) automatically as described above.
- *./data/ingredients.csv* - a list of ingredients and their corresponding items and categories.  Ingredients are the constituents of cocktails as described on thecocktaildb.com.  Items are generic names for these constituents and are how these are understood by the local cabinet.  Several ingredients fall within one item.  For example 'whisky' and 'scotch' are both names as ingredients in different recipies on thecocktaildb.com.  These are essentially different names for the same thing and so both are recorded as 'whisky' in the local cabinet.  This file operates as an interpreter enabling a list of ingredients to be described as a list of items or vice versa.  Categories are types of items/ingredients.  For example 'spirits'.

#### Usage:

Usage is intended to be simple.  The app has two sections, in a standard web browser each are divided into a left and right panel although this layout changes on some smaller devices:
1. **Cocktails** 
- On the left are a list of cocktails on the left side.  Cocktails for which the user has ingredients are presented in bolder type, those where at least one ingredient is lacking are in lighter type.  A slider at the top allows the user to determine the maximum number of missing ingredients there might for each cocktail before it is removed from the list.  A search bar below allows textual search of showing cocktail names.  By deafult the slider is set such that only cocktails for which the cabinet contains all ingredients are shown.
- On the right is initially a placeholder logo.  When the user clicks on the name of one of the cocktails on the left this is replaced with the cocktail recipe.  In this recipie any ingredient missing from the cabinet is shown in light text.
2. **Cabinet**

