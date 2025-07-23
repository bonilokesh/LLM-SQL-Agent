import pandas as pd
import sqlite3
import os

def load_excel_to_db():
    # Step 1: Create or connect to SQLite DB
    os.makedirs("db", exist_ok=True)  # Make sure the folder exists
    conn = sqlite3.connect("db/ecommerce.db")  # This creates the DB if it doesn't exist

    # Step 2: Map file names to table names
    files = {
            "eligibility": r"D:\anarix\data\eligibility.xlsx",
            "total_sales": r"D:\anarix\data\total_sales.xlsx",
           "ad_sales": r"D:\anarix\data\ad_sales.xlsx"
    }

    # Step 3: Read Excel and load into database
    for table_name, file_path in files.items():
        if os.path.exists(file_path):
            df = pd.read_excel(file_path)
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            print(f"Loaded '{table_name}' into database.")
        else:
            print(f"Missing file: {file_path}")

    conn.close()
    print("Done! Database created at db/ecommerce.db")

if __name__ == "__main__":
    load_excel_to_db()
