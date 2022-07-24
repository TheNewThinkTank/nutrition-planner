"""_summary_
"""

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

    return response.text


st.write(get_facts(ingredient, amount, unit))
