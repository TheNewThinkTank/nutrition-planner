"""_summary_
"""

import pandas as pd

# from pprint import pprint as pp

# from nutrition_facts import nutrition_facts_100g


"""
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
        carbs = ""
        fat = ""
        protein = ""

        return carbs, fat, protein

    def get_micros(self):

        fat_unsaturated = ""
        fiber = ""
        amino_acids = ""
        minerals = ""
        vitamins = ""

        return fat_unsaturated, fiber, amino_acids, minerals, vitamins
"""


def main():
    """_summary_"""

    snack = {}
    breakfast = {}
    lunch = {}
    dinner = {"Broccoli": "100g", "Chicken breast": "300g", "Brown rice": "180g"}
    cheat_meal = {}

    # dinner = Meal({"Broccoli": "100g", "Chicken breast": "300g", "Brown rice": "180g"})
    # all_facts = dinner.get_all_facts()
    # print(all_facts)
    # dinner.get_macros()
    # dinner.get_micros()

    def get_df(ingredient):
        return pd.read_csv(
            f"data/{ingredient}.csv", skiprows=range(6), skipfooter=4, engine="python"
        )

    df_broccoli = get_df("broccoli_raw")
    print(df_broccoli)


if __name__ == "__main__":
    main()
