"""_summary_
"""

import asyncio
import json
import time

import httpx
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.title("Nutrition App")
st.write(
    """
## Analyze the nutritional content of your meals
Created by Gustav C. Rasmussen. Powered by nutritionix
"""
)

number_of_ingredients = st.sidebar.text_input("Number of main ingredients in your meal")
ingredients = {}
for i in range(1, int(number_of_ingredients) + 1):
    ingredient = st.sidebar.text_input(f"Ingredient_{i}")
    amount = st.sidebar.text_input(f"Amount_{i}")
    unit = st.sidebar.text_input(f"Unit_{i}")
    ingredients[ingredient] = amount, unit

URL = "https://trackapi.nutritionix.com/v2/natural/nutrients"
HEADER = {
    "Content-Type": "application/json",
    "x-app-id": st.secrets["NUTRITIONIX_ID"],
    "x-app-key": st.secrets["NUTRITIONIX_KEY"],
}

nutrition = {"protein": 0, "fat": 0, "carbs": 0}


async def get_nutritionix(client, body):
    r = await client.post(URL, json=body)
    # assert r.status_code == 200
    r = json.loads(r.text)["foods"][0]
    nutrition["protein"] += r["nf_protein"]
    nutrition["fat"] += r["nf_total_fat"]
    nutrition["carbs"] += r["nf_total_carbohydrate"]
    return nutrition


async def main():
    async with httpx.AsyncClient(headers=HEADER) as client:
        tasks = []
        for k, v in ingredients.items():
            BODY = {"query": f"{v[0]}{v[1]} of {k}", "timezone": "US/Eastern"}
            tasks.append(asyncio.create_task(get_nutritionix(client, BODY)))
        macros = await asyncio.gather(*tasks)
        return macros


start_time = time.time()
macros = asyncio.run(main())
print(f"Calls to the Nutritionix API took: {time.time() - start_time} seconds")

st.write(
    f"Meal macros: Protein: {macros['protein']:.1f} g,"
    f" Fat: {macros['fat']:.1f} g,"
    f" Carbs: {macros['carbs']:.1f} g"
)

plt.style.use("dark_background")
fig1, ax1 = plt.subplots()
labels = "protein", "fat", "carbohydrate"
sizes = [macros["protein"], macros["fat"], macros["carbs"]]
colors = sns.color_palette("pastel")[0:3]
ax1.pie(
    sizes,
    labels=labels,
    colors=colors,
    autopct="%1.1f%%",
)
ax1.axis("equal")
st.pyplot(fig1)
