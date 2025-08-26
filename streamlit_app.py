# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests


cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title(f"Customize Your Smoothie! :cup_with_straw:")
st.write(
  """
    Choose the fruits you want in your custom Smoothie!
  """
)

title = st.text_input("Name on Smoothie :")

my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
# st.dataframe(my_dataframe)

ingredients = st.multiselect(
    "Choose upto 5 Ingredients : ",
    my_dataframe,
    max_selections=5
)

submit_button = st.button("Submit Order")

if title and submit_button:
    # st.write(ingredients)
    ingredients_str = ''
    for fruit in ingredients:
        ingredients_str += fruit + ' '
    my_insert_stmt =f"""
            insert into smoothies.public.orders(NAME_ON_ORDER,ingredients)
            values ('{title}','{ingredients_str}')
            """
    # st.write(my_insert_stmt)
    session.sql(my_insert_stmt).collect()
    st.success(f'Your Smoothie is ordered! , {title}', icon="✅")


smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())