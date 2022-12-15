import cocktails, cabinet, queries, saveloadexit
import pickle, os, sys, csv



def main():
    global cocktail_dictionary
    cocktail_dictionary = saveloadexit.load_cocktails()
    global drinks_cabinet
    drinks_cabinet = cabinet.Cabinet()
    drinks_cabinet.load()
    global assumed
    assumed = saveloadexit.load_assumed()
    os.system("clear")
    print("COCKTAIL CABINET!")
    while True:
        # reload the cocktail dictionary to reflect any changes
        cocktail_dictionary = saveloadexit.load_cocktails()
        print("\nMAIN MENU")
        step = input("View 'cabinet', find 'cocktails', manage 'settings', or 'exit': ")
        if step.lower() == "cabinet":
            view_cabinet()
        elif step.lower() == "cocktails":
            find_cocktails()
        elif step.lower() == "settings":
            manage_settings(assumed)
            pass
        elif step.lower() == "exit":
            exit()
        else:
            pass


def view_cabinet():
    print("\nDRINKS CABINET")
    while True:
        command = input(
            ("Either 'add', 'remove', 'list' or 'clear' items, or go 'back': ")
        ).lower()
        if command == "add":
            while True:
                drinks_cabinet.list_have()
                print(" ")
                item = input("Enter ingredient to add, or go 'back': ").title()
                if item == "Back":
                    break
                else:
                    drinks_cabinet.add(item)
        elif command == "remove":
            item = input("Enter ingredient to remove: ").title()
            drinks_cabinet.remove(item)
        elif command == "list":
            while True:
                option = input(
                    "List ingredients that 'are' in the cabinet, those that 'aren't', go 'back': "
                ).lower()
                if option == "are":
                    print(" ")
                    drinks_cabinet.list_have()
                    print(" ")
                elif option == "aren't":
                    print(" ")
                    drinks_cabinet.list_dont_have()
                    print(" ")
                elif option == "back":
                    break
                else:
                    pass
        elif command == "clear":
            drinks_cabinet.clear()
        elif command == "back":
            drinks_cabinet.save()
            break
        else:
            pass


def find_cocktails():
    print("\nCOCKTAILS")
    while True:
        command = input(
            (
                "List drinks you 'have' ingredients for, include those where 'one' or 'two' ingredients are missing, list 'all' cocktails or go 'back': "
            )
        ).lower()
        if command == "have":
            drinks_cabinet.list_have()
            print(" ")
            drinks = queries.find_cocktails(
                cocktail_dictionary, drinks_cabinet, assumed, 0
            )
            queries.print_cocktails(drinks)
            print(" ")
        elif command == "one":
            drinks_cabinet.list_have()
            print(" ")
            drinks = queries.find_cocktails(
                cocktail_dictionary, drinks_cabinet, assumed, 1
            )
            queries.print_cocktails(drinks)
            print(" ")
        elif command == "two":
            drinks_cabinet.list_have()
            print(" ")
            drinks = queries.find_cocktails(
                cocktail_dictionary, drinks_cabinet, assumed, 2
            )
            queries.print_cocktails(drinks)
            print(" ")
        elif command == "all":
            print(" ")
            drinks = queries.find_cocktails(
                cocktail_dictionary, drinks_cabinet, assumed, 10
            )
            queries.print_cocktails(drinks)
            print(" ")
        elif command == "back":
            break
        else:
            pass


def manage_settings(assumed):
    print("\nSETTINGS")
    while True:
        command = input(
            ("'Refresh' cocktail list, change 'assumed' items or go 'back': ")
        ).lower()
        if command == "refresh":
            cocktail_dictionary = saveloadexit.load_cocktails()
            while True:
                if (
                    input(
                        f"The cocktail list currently includes {len(cocktail_dictionary)} drinks. If you refresh you will lose these, are you sure? "
                    ).lower()
                    == "yes"
                ):
                    cocktail_dictionary = cocktails.get_cocktails()
                    saveloadexit.save_cocktails(cocktail_dictionary)
                    break
                else:
                    break
        elif command == "assumed":
            while True:
                items = ", ".join(assumed)
                print(f"Items assumed to be available: {items}")
                sub_command = input("'Add' or 'remove' assumed items, or go 'back': ")
                if sub_command == "add":
                    try:
                        item = input("Item to add: ").title()
                        assumed.append(item)
                    except ValueError:
                        pass
                elif sub_command == "remove":
                    try:
                        item = input("Item to remove: ").title()
                        assumed.remove(item)
                    except ValueError:
                        pass
                elif sub_command == "back":
                    break
                else:
                    pass
        elif command == "back":
            break
        else:
            pass




if __name__ == "__main__":
    main()
