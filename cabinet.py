import csv


class Cabinet:
    def __init__(self):
        self.items = return_items()
        self.inventory = dict.fromkeys(sorted(list(self.items)), False)
        
    def __str__(self):
        return f"{self.inventory}"  
        
    def save(self):
        with open("cabinet.csv", "w") as file:
            writer = csv.DictWriter(file, fieldnames=["item", "have"])
            writer.writeheader()
            for key in self.inventory:
                writer.writerow({"item":key, "have":self.inventory[key]})

    def load(self):
        with open("cabinet.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["have"] == "True":
                    self.inventory[row["item"]] = True
                else:
                    self.inventory[row["item"]] = False
                    
    def add(self, ingredient):
        if ingredient in self.inventory:
                self.inventory[ingredient] = True
                print(f"Added {ingredient}")
        else:
            print("Ingredient not found")

    def remove(self, ingredient):
        self.ingredient = ingredient
        if self.ingredient in self.inventory:
                self.inventory[self.ingredient] = False
                print(f"Removed {self.ingredient}")
        else:
            print("Ingredient not found")
                      
    def list_have(self):
        if any(self.inventory.values()):
            items = []
            for key in self.inventory:
                if self.inventory[key]:
                    items.append(key)
            items = ", ".join(items)
            print(f"Cabinet contains: {items}")
        else:
            print("Cabinet is empty")

    def list_dont_have(self):
        items = []
        for key in self.inventory:
            if self.inventory[key] == False:
                items.append(key)
        items = ", ".join(items)
        print(f"Cabinet does not contain: {items}")

    def clear(self):
        if input("Are you sure you want to clear the cabinet? ").lower() == "yes":
            for key in self.inventory:
                self.inventory[key] = False
            print("Cabinet cleared")
        


"""returns a set of items"""
def return_items():
    items = set()
    with open("categorisation.csv", "r", encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
           items.add(row[2])
    return items
