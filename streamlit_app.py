# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

cnx = st.connection("snowflake")
# Write directly to the app
st.title(":cup_with_straw: Customise your smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom **smoothie**
    """
)

name_on_order = st.text_input('Name on smoothie:')
st.write('The name of your smoothie will be: ', name_on_order)

#session = get_active_session()
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose upto 5 ingredients",
    my_dataframe,
    max_selections=5
)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''
    for fruits_chosen in ingredients_list:
        ingredients_string += fruits_chosen + ' '

    st.write(ingredients_string)

    my_insert_stmt = """insert into smoothies.public.orders(name_on_order, ingredients)
                         values ('""" + name_on_order + """','""" + ingredients_string + """')"""
    #st.write(my_insert_stmt)
    #st.stop()

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        success_msg = 'Your Smoothie is ordered, ' + name_on_order
        st.success(success_msg, icon="✅")
