"""_summary_
"""

# from pprint import pprint as pp

from nutrition_facts import nutrition_facts_100g


class Meal:
    def __init__(self, ingredients: dict) -> None:
        self.ingredients = {
            k.lower().replace(" ", "_"): v for k, v in ingredients.items()
        }

    def get_all_facts(self) -> dict:
        all_facts = {}
        for ingredient in self.ingredients.keys():
            ingredient_facts = nutrition_facts_100g[ingredient]
            all_facts[ingredient] = ingredient_facts
        return all_facts

    def get_macros(self):
        pass

    def get_micros(self):
        pass


def main():
    """_summary_"""

    dinner = Meal({"Broccoli": "100g", "Chicken breast": "300g", "Brown rice": "180g"})
    all_facts = dinner.get_all_facts()
    print(all_facts)
    dinner.get_macros()
    dinner.get_micros()


if __name__ == "__main__":
    main()
