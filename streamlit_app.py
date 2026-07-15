# Streamlit smoothie customizer app with Snowpark session
# Co-authored with CoCo
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!"""
)

##add selectbox
#option = st.selectbox(
 #   "What is your favorite fruit?",
 #)

#name on order 
name_on_order = st.text_input ('Name on Smoothie:')
st.write('The name on your smoothie will be:', name_on_order)


#st.write("Your favorite fruit is:", option)
from snowflake.snowpark.functions import col
#display the fruit options list in SiS
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select("FRUIT_NAME")
pd_df = my_dataframe.to_pandas()
#st.dataframe(data=pd_df, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    pd_df["FRUIT_NAME"].tolist(),
    max_selections=5
)

if ingredients_list:
    num_selected = len(ingredients_list)
    remaining = 5 - num_selected
    if remaining > 0:
        st.info(f"You have {remaining} fruit(s) left to add.")
    else:
        st.success("You have selected the maximum of 5 fruits!")

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    st.write(my_insert_stmt)

    if st.button("Submit Order"):
        session.sql(my_insert_stmt).collect()
        st.success("Your S
