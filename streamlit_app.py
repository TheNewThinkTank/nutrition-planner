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
try:
    num_ingredients = int(number_of_ingredients)
except:
    st.stop()

ingredients = {}
for i in range(1, int(number_of_ingredients) + 1):
    ingredient = st.sidebar.text_input(f"Ingredient_{i}")
    amount = st.sidebar.text_input(f"Amount_{i}")
    unit = st.sidebar.text_input(f"Unit_{i}")
    ingredients[ingredient] = amount, unit
    try:
        food = str(ingredient)
        qty = int(amount)
        unt = str(unit)
    except:
        st.stop()

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
    return


async def main():
    async with httpx.AsyncClient(headers=HEADER) as client:
        tasks = []
        for k, v in ingredients.items():
            BODY = {"query": f"{v[0]}{v[1]} of {k}", "timezone": "US/Eastern"}
            tasks.append(asyncio.create_task(get_nutritionix(client, BODY)))
        macros = await asyncio.gather(*tasks)
        return


start_time = time.time()
asyncio.run(main())

st.write(
    f"Meal macros: Protein: {nutrition['protein']:.1f} g,"
    f" Fat: {nutrition['fat']:.1f} g,"
    f" Carbs: {nutrition['carbs']:.1f} g"
)

st.write(
    "Calls to the Nutritionix API took a total of: "
    f"{time.time() - start_time:.1f} seconds"
)

plt.style.use("dark_background")
fig1, ax1 = plt.subplots()
labels = "protein", "fat", "carbohydrate"
sizes = [nutrition["protein"], nutrition["fat"], nutrition["carbs"]]
colors = sns.color_palette("pastel")[0:3]
"""
ax1.pie(
    sizes,
    labels=labels,
    colors=colors,
    autopct="%1.1f%%",
)
ax1.axis("equal")
"""

# sns.set_theme(style="whitegrid")
tips = sns.load_dataset("tips")
ax = sns.barplot(x=labels, y=sizes)  # colors=colors, data=tips)

st.pyplot(fig1)
