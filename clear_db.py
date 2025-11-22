import sqlite3
conn = sqlite3.connect('hospital.db')
cursor = conn.cursor()

# Delete unnecessary tables
drop_tables = ["Staff", "Appointment", "Pharmacy", "Inventory"]
for t in drop_tables:
    cursor.execute(f"DROP TABLE IF EXISTS {t}")
    print(f"🗑️ Dropped table: {t}")

conn.commit()
conn.close()
print("✅ Unnecessary tables removed successfully!")
