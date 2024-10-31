import asyncio
import time
import json

import httpx
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.title("Nutrition App")
st.write(
    """
## Analyze the nutritional content of your meals
Created by Gustav C. Rasmussen. Powered by Nutritionix
"""
)

# Set up input and validation for ingredients
ingredients = []
with st.sidebar:
    st.write("### Add Ingredients")
    num_ingredients = st.number_input("Number of ingredients", min_value=1, value=1, step=1)

    for i in range(num_ingredients):
        with st.expander(f"Ingredient {i + 1}"):
            ingredient = st.text_input(f"Name of ingredient {i + 1}")
            amount = st.number_input(f"Amount for ingredient {i + 1}", min_value=0.0, step=1.0)
            unit = st.selectbox(f"Unit for ingredient {i + 1}", ["g", "ml", "oz", "cup", "tbsp"])
            if ingredient and amount:
                ingredients.append((ingredient, amount, unit))

# Nutritionix API configuration
URL = "https://trackapi.nutritionix.com/v2/natural/nutrients"
HEADER = {
    "Content-Type": "application/json",
    "x-app-id": st.secrets["NUTRITIONIX_ID"],
    "x-app-key": st.secrets["NUTRITIONIX_KEY"],
}

# Define nutrient totals
nutrition = {"protein": 0, "fat": 0, "carbs": 0}


async def get_nutritionix(client, body):
    r = await client.post(URL, json=body)
    r = json.loads(r.text)["foods"][0]
    return {
        "protein": r["nf_protein"],
        "fat": r["nf_total_fat"],
        "carbs": r["nf_total_carbohydrate"]
    }


async def main(ingredients):
    nutrition = {"protein": 0, "fat": 0, "carbs": 0}
    async with httpx.AsyncClient(headers=HEADER) as client:
        tasks = []
        for ingredient, amount, unit in ingredients:
            body = {"query": f"{amount}{unit} of {ingredient}", "timezone": "US/Eastern"}
            tasks.append(get_nutritionix(client, body))
        results = await asyncio.gather(*tasks)
        for result in results:
            nutrition["protein"] += result["protein"]
            nutrition["fat"] += result["fat"]
            nutrition["carbs"] += result["carbs"]
    return nutrition


# Run the main function and calculate time
start_time = time.time()
asyncio.run(main(ingredients))
st.write(f"Meal macros: Protein: {nutrition['protein']:.1f} g, Fat: {nutrition['fat']:.1f} g, Carbs: {nutrition['carbs']:.1f} g")
st.write(f"API calls took a total of: {time.time() - start_time:.1f} seconds")

# Display chart
fig, ax = plt.subplots()
sns.barplot(x=["Protein", "Fat", "Carbs"], y=[nutrition["protein"], nutrition["fat"], nutrition["carbs"]], ax=ax)
ax.set_title("Macronutrient Breakdown")
ax.set_ylabel("Grams")
st.pyplot(fig)
