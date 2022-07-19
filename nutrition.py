"""_summary_
"""

import pandas as pd
import re

# from pprint import pprint as pp

import lookup

# from nutrition_facts import nutrition_facts_100g


class Meal:
    def __init__(self, ingredients: dict) -> None:
        self.ingredients = {
            k.lower().replace(" ", "_"): v for k, v in ingredients.items()
        }
        self.dfs = {}

    def get_df(self):
        for ingredient in self.ingredients.keys():
            df = pd.read_csv(
                f"data/{ingredient}.csv",
                skiprows=range(6),
                skipfooter=4,
                engine="python",
            )
            self.dfs[ingredient] = df

        return self.dfs

    def calc_nutrients_from_amount(self):
        regex = r"(\d*)\s?([a-zA-Z]*)"

        for value in self.ingredients.values():
            res = re.search(regex, value)
            amount, unit = res.group(1), res.group(2)
            factor = float(amount) / 100

            protein_100g = self.dfs["broccoli_raw"][
                self.dfs["broccoli_raw"]["Nutrient"] == "Protein"
            ]

            protein_100g_amount = protein_100g["Amount"]
            protein_100g_unit = protein_100g["Unit"]

            protein_actual = (
                protein_100g_amount
                * lookup.WeightUnit[protein_100g_unit.values[0].upper()].value
                * factor
                * lookup.WeightUnit[unit.upper()].value
            )
            return f"{protein_actual.values[0]:.2f} g"

    def get_all_facts(self) -> dict:
        all_facts = {}
        """
        for ingredient in self.ingredients.keys():
            ingredient_facts = nutrition_facts_100g[ingredient]
            all_facts[ingredient] = ingredient_facts
        """
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


def main():
    """_summary_"""

    # snack = {'walnuts': '20g', 'dates': '30g'}
    # breakfast = {'oatmeal': '80g', 'milk': '120g'}
    # lunch = {'ryebread': '100g', 'salmon': '75g', 'olive oil': '1g'}
    dinner_content = {
        "Broccoli raw": "120g",
        # "Chicken raw ground": "300g",
        # "Brown rice": "180g",
    }
    # cheat_meal = {'wholegrain pancakes': '200g', 'Acacia honey': '5g'}

    dinner = Meal(dinner_content)
    dfs = dinner.get_df()
    # print(dfs["broccoli_raw"])
    # print(dfs["broccoli_raw"].dtypes)

    protein = dinner.calc_nutrients_from_amount()
    print("protein: ", protein)

    # dinner.calc_nutrients_from_amount()

    # all_facts = dinner.get_all_facts()
    # print(all_facts)
    # dinner.get_macros()
    # dinner.get_micros()


if __name__ == "__main__":
    main()
