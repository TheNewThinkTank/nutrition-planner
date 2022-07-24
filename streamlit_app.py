"""_summary_
"""

import streamlit as st

st.title("Nutrition App")

st.write(
    """
# Analyze the nutritional content of your meals
Created by Gustav C. Rasmussen. Powered by nutritionix
"""
)

# dish = st.radio("Pick a dish", ["succotash", "curried pumpkin soup"])

st.sidebar.text_input("Ingredient")
st.sidebar.text_input("Amount")
st.sidebar.text_input("Unit")
