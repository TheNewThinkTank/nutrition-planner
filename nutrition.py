"""_summary_
"""

from pprint import pprint as pp

from nutrition_facts import nutrition_facts_100g


def main():
    """_summary_"""
    INGREDIENT = "Broccoli"
    ingredient_facts = nutrition_facts_100g[INGREDIENT.lower()]
    pp(ingredient_facts)


if __name__ == "__main__":
    main()
