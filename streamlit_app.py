"""_summary_
"""

import json
import requests
import streamlit as st

st.title("Nutrition App")

st.write(
    """
# Analyze the nutritional content of your meals
Created by Gustav C. Rasmussen. Powered by nutritionix
"""
)

ingredient = st.sidebar.text_input("Ingredient")
amount = st.sidebar.text_input("Amount")
unit = st.sidebar.text_input("Unit")


URL = "https://trackapi.nutritionix.com/v2/natural/nutrients"

HEADER = {
    "Content-Type": "application/json",
    "x-app-id": st.secrets["NUTRITIONIX_ID"],
    "x-app-key": st.secrets["NUTRITIONIX_KEY"],
}


def get_facts(ingredient, amount, unit):
    BODY = {"query": f"{amount}{unit} of {ingredient}", "timezone": "US/Eastern"}

    response = requests.post(
        URL,
        headers=HEADER,
        json=BODY,
    )

    # r = response.text["foods"]
    """
    return (
        r["foods"],
        r["serving_qty"],
        r["serving_unit"],
        r["nf_calories"],
        r["nf_total_fat"],
        r["nf_saturated_fat"],
        r["nf_cholesterol"],
        r["nf_sodium"],
        r["nf_total_carbohydrate"],
        r["nf_dietary_fiber"],
        r["nf_sugars"],
        r["nf_protein"],
    )
    """
    return json.dumps(response.text)


st.write(get_facts(ingredient, amount, unit))
