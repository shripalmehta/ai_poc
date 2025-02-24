import pandas as pd
import sqlite3

# Load the Excel file (replace 'data.xlsx' with your actual filename)
file_path = "../data/file_out.csv"
df = pd.read_csv(file_path)

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("../data/database.db")
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    UniqueID INTEGER PRIMARY KEY,
    DocumentID INTEGER,
    Date TEXT,
    SKU INTEGER,
    Price REAL,
    Discount REAL,
    Customer INTEGER,
    Quantity INTEGER
)
''')

# Insert data into the table
df.to_sql("sales", conn, if_exists="append", index=False)

# Commit and close connection
conn.commit()
conn.close()

print("Data successfully stored in SQLite database.")