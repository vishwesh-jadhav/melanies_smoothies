
# import streamlit as st
# from snowflake.snowpark.functions import col
# import requests

# st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
# st.write("""Choose the fruits you want in your custom Smoothie!""")

# # Name on order input
# name_on_order = st.text_input('Name on Smoothie:')
# st.write('The name on your Smoothie will be:', name_on_order)

# # Snowflake session
# cnx = st.connection("snowflake")
# session = cnx.session()
# st.my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

# # Multiselect for ingredients
# ingredients_list = st.multiselect(
#     'Choose up to 5 ingredients:',
#     my_dataframe,
#     max_selections=5
# )

# # If ingredients are selected, display them and construct the insert statement
# if ingredients_list:
#     ingredients_string = ' '.join(ingredients_list)
#     st.subheader(fruit_chosen + 'Nutrition Information')
#     st.write(ingredients_string)
    
#     my_insert_stmt = f""" 
#         INSERT INTO smoothies.public.orders(name_on_order, ingredients, order_filled)
#         VALUES ('{name_on_order}', '{ingredients_string}', FALSE)
#     """
    
#     st.write(my_insert_stmt)
    
#     # Submit order
#     time_to_insert = st.button('Submit Order')
    
#     if time_to_insert:
#         session.sql(my_insert_stmt).collect()
#         st.success('Your Smoothie is ordered!', icon="✅")
#         st.rerun()  # Refresh the app to show updated orders


# smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)  

import streamlit as st
from snowflake.snowpark.functions import col
import requests

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Name on order input
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Snowflake session
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch data from Snowflake table and convert to Pandas DataFrame
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON')).to_pandas()

#  Display the table
# st.dataframe(data=my_dataframe, use_container_width=True)
#  Stop execution here to verify the table
# st.stop()

# Correctly assign the Pandas DataFrame
pd_df = my_dataframe  # Since `my_dataframe` is already converted to Pandas earlier
st.dataframe(pd_df, use_container_width=True)

# Stop execution here to verify the table
st.stop()


# Multiselect for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe['FRUIT_NAME'],  # Correctly specify column for selection
    max_selections=5
)

# If ingredients are selected, display them and construct the insert statement
if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)  # Correctly format ingredients as a comma-separated string
    search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
    st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
    st.subheader("Nutrition Information for Selected Ingredients")
    st.write(ingredients_string)

    # Create the SQL insert statement
    my_insert_stmt = f""" 
        INSERT INTO smoothies.public.orders(name_on_order, ingredients, order_filled)
        VALUES ('{name_on_order}', '{ingredients_string}', FALSE)
    """
    st.write(my_insert_stmt)

    # Submit order
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        try:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
            st.rerun()  # Refresh the app to show updated orders
        except Exception as e:
            st.error(f"Something went wrong: {e}")

# API call for external data
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")

# Check if the request was successful
if smoothiefroot_response.status_code == 200:
    # Display API response as a DataFrame
    api_data = smoothiefroot_response.json()
    st.dataframe(data=api_data, use_container_width=True)
else:
    st.error("Failed to fetch data from SmoothieFroot API")


