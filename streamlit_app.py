# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd


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

my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"),col("SEARCH_ON"))
pd_df = my_dataframe.to_pandas()

# st.dataframe(my_dataframe)
# st.dataframe(pd_df)
# st.stop()

ingredients = st.multiselect(
    "Choose upto 5 Ingredients : ",
    my_dataframe,
    max_selections=5
)

submit_button = st.button("Submit Order")

if submit_button and ingredients:
    # st.write(ingredients)
    ingredients_str = ''
    for fruit in ingredients:
        ingredients_str += fruit + ' '
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', fruit,' is ', search_on, '.')
        st.subheader(fruit + ' Nutrition Information')
        smoothiefroot = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        # st.write(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        sf_df = st.dataframe(data = smoothiefroot.json(),use_container_width = True)
        
    # st.write(ingredients)
    my_insert_stmt =f"""
            insert into smoothies.public.orders(NAME_ON_ORDER,ingredients)
            values ('{title}','{ingredients_str}')
            """
    # st.write(my_insert_stmt)
    session.sql(my_insert_stmt).collect()
    st.success(f'Your Smoothie is ordered! , {title}', icon="✅")





