import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime

# ================== DATABASE CONNECTION ==================
def get_connection():
    return mysql.connector.connect(
        host="bukqxhgtpvn4hogiklcv-mysql.services.clever-cloud.com",
        user="uq1cmnqukpjg7gpa",
        password="odV2Yp3EwqIaUFpx64vN",
        database="bukqxhgtpvn4hogiklcv",
        port=3306
    )

conn = get_connection()
cursor = conn.cursor(dictionary=True)

# ================== PAGE SETTINGS ==================
st.set_page_config(page_title="Hospital Management System", page_icon="🏥", layout="wide")
st.title("🏥Hospital Management System")

# ================== FETCH TABLES ==================
cursor.execute("SHOW TABLES;")
tables = cursor.fetchall()
all_tables = [list(row.values())[0] for row in tables]

# Emojis for better UI
emoji_map = {
    "Patient": "🧍",
    "Employee": "💼",
    "Doctor": "👨‍⚕️",
    "Nurse": "👩‍⚕️",
    "Receptionist": "💁‍♀️",
    "Room": "🏥",
    "Medicine": "💊",
    "Equipment": "⚙️",
    "Record": "📋",
    "Assigned": "🧩",
    "Attends": "🤝",
    "Maintains": "🗂️",
    "Governs": "🩺",
    "BilledFor": "💰"
}

# Sidebar menu
menu = ["🏠 Home", "📊 View Database"] + [f"{emoji_map.get(t.capitalize(), '📦')} {t}" for t in all_tables]
choice = st.sidebar.selectbox("Select Option", menu)

# ================== HOME PAGE ==================
if choice == "🏠 Home":
    st.write("""
    ### 👋 Welcome to Hospital Management System
    This platform allows you to:
    - 🧍 Register patients  
    - 👨‍⚕️ Add doctors and staff  
    - 🏥 Manage rooms and facilities  
    - 💊 Track medicines and equipment  
    - 📋 Maintain medical and billing records  
    - 📊 View and manage all tables dynamically  
    """)

# ================== VIEW DATABASE PAGE ==================
elif choice == "📊 View Database":
    st.subheader("📊 Dynamic Database Viewer")

    selected_table = st.selectbox("Select Table to View", all_tables)
    df = pd.read_sql(f"SELECT * FROM {selected_table}", conn)

    # 🔍 Smart Search / Filter
    st.write("### 🔍 Search Table Records")

    columns = df.columns.tolist()
    selected_col = st.selectbox("Select column to search in", columns)
    search = st.text_input("Enter keyword")

    if search:
        df_filtered = df[df[selected_col].astype(str).str.lower() == search.lower()]

        st.dataframe(df_filtered, hide_index=True)
        st.caption(f"Showing {len(df_filtered)} matching record(s) in column '{selected_col}'")
    else:
        st.dataframe(df, hide_index=True)
        st.caption(f"Showing all {len(df)} record(s)")

# ================== ADD / MANAGE DATA PAGE ==================
else:
    table_name = choice.split(" ", 1)[1]
    st.subheader(f"{choice} — Add New Record")

    cursor.execute(f"DESCRIBE {table_name}")
    columns = cursor.fetchall()

    input_data = {}
    for col in columns:
        col_name = col["Field"]
        col_type = col["Type"].upper()
        if "PRI" in col["Key"]:
            continue

        if "SEX" in col_name.lower() or "GENDER" in col_name.lower():
            input_data[col_name] = st.selectbox(f"{col_name}", ["Male", "Female", "Other"])
        elif "DATE" in col_name.lower():
            date_val = st.date_input(f"{col_name}")
            input_data[col_name] = date_val.strftime("%Y-%m-%d")
        elif "INT" in col_type:
            input_data[col_name] = st.number_input(f"{col_name}", step=1)
        elif "FLOAT" in col_type or "DOUBLE" in col_type:
            input_data[col_name] = st.number_input(f"{col_name}", format="%.2f")
        else:
            input_data[col_name] = st.text_input(f"{col_name}")

    if st.button(f"Add Record to {table_name}"):
        if input_data:
            cols = ", ".join(input_data.keys())
            placeholders = ", ".join(["%s"] * len(input_data))
            values = list(input_data.values())
            try:
                cursor.execute(f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})", values)
                conn.commit()
                st.success(f"✅ Record added successfully to {table_name}!")
            except Exception as e:
                st.error(f"⚠️ Error: {e}")

        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        st.markdown("---")
        st.dataframe(df, hide_index=True)

conn.close()


