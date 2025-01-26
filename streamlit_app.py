import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!""")

# Name on order input
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Snowflake session
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Multiselect for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
    )

# If ingredients are selected, display them and construct the insert statement
if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)
    st.write(ingredients_string)
    
    my_insert_stmt = f""" 
        INSERT INTO smoothies.public.orders(name_on_order, ingredients, order_filled)
        VALUES ('{name_on_order}', '{ingredients_string}', FALSE)
    """
    
    st.write(my_insert_stmt)
    
    # Submit order
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        st.rerun()  # Refresh the app to show updated orders

