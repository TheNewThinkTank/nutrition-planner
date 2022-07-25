"""_summary_
"""

import json

import matplotlib.pyplot as plt
import requests
import seaborn as sns
import streamlit as st

st.title("Nutrition App")
st.write(
    """
# Analyze the nutritional content of your meals
Created by Gustav C. Rasmussen. Powered by nutritionix
"""
)

number_of_ingredients = 2

for i in range(number_of_ingredients):
    # st.write(i)

    ingredient = st.sidebar.text_input(f"Ingredient_{i}")
    amount = st.sidebar.text_input(f"Amount_{i}")
    unit = st.sidebar.text_input(f"Unit_{i}")


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

    r = json.loads(response.text)["foods"][0]

    return {
        "food_name": r["food_name"],
        "serving_qty": r["serving_qty"],
        "serving_unit": r["serving_unit"],
        "calories": r["nf_calories"],
        "total_fat": r["nf_total_fat"],
        "saturated_fat": r["nf_saturated_fat"],
        "cholesterol": r["nf_cholesterol"],
        "sodium": r["nf_sodium"],
        "total_carbohydrate": r["nf_total_carbohydrate"],
        "dietary_fiber": r["nf_dietary_fiber"],
        "sugars": r["nf_sugars"],
        "protein": r["nf_protein"],
    }


nutrition = get_facts(ingredient, amount, unit)
st.write(nutrition)

plt.style.use("dark_background")
fig1, ax1 = plt.subplots()
labels = "protein", "fat", "carbohydrate"
sizes = [nutrition["protein"], nutrition["total_fat"], nutrition["total_carbohydrate"]]
colors = sns.color_palette("pastel")[0:3]
ax1.pie(
    sizes,
    labels=labels,
    colors=colors,
    autopct="%1.1f%%",
)
ax1.axis("equal")
st.pyplot(fig1)
