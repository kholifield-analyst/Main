import streamlit as st
import snowflake.connector
import pandas as pd

sf_user = st.secrets["snowflake"]["user"]
sf_password = st.secrets["snowflake"]["password"]
sf_account = st.secrets["snowflake"]["account"]
sf_warehouse = st.secrets["snowflake"]["warehouse"]
sf_database = st.secrets["snowflake"]["database"]
sf_schema = st.secrets["snowflake"]["schema"]

conn = snowflake.connector.connect(
    user=sf_user,
    password=sf_password,
    account=sf_account,
    warehouse=sf_warehouse,
    database=sf_database,
    schema=sf_schema)
#Get Data from snowflake
cursor = conn.cursor()
query = "SELECT * FROM ACT_DEV_DISCOUNTRATE_DB.WORKSPACE.DR_USER_INPUT limit 23;"
cursor.execute(query)

data = cursor.fetchall()


cursor.close()
conn.close()

#Building ("Calculator")
st.title("Smith-Wilson UFR Finder:chart_with_upwards_trend:")
columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(data, columns=columns)
st.dataframe(df)

#Approve & Edit

def get_user_role():
    try:
        conn = snowflake.connector.connect(
            user=sf_user,
    password=sf_password,
    account=sf_account,
    warehouse=sf_warehouse,
    database=sf_database,
    schema=sf_schema)
        
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_ROLE()")
        role_tuple = cursor.fetchone()
        cursor.close()
        conn.close()
        if role_tuple and role_tuple[0]:
            return role_tuple[0]
        else:
            return None
    
    except Exception as e:
        st.error(f"Error fetching user role: {str(e)}")
        return None
    
def show_buttons_based_on_role(role):
    if role == 'ACCOUNTADMIN':
        approve_button = st.button('Approve')
        

    if role == 'ACT_DEV_DISCOUNTRATE_DB_USER_ROLE':
            edit_button = st.button('Edit:pencil:')

user_role = get_user_role()
if user_role:
    st.write(f'Logged in with role: {user_role}')
    show_buttons_based_on_role(user_role)
