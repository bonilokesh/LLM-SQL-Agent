import pandas as pd
import sqlite3
import os

def load_excel_to_db():

    os.makedirs("db", exist_ok=True) 
    conn = sqlite3.connect("db/ecommerce.db")  
    files = {
            "eligibility": r"D:\anarix\data\eligibility.xlsx",
            "total_sales": r"D:\anarix\data\total_sales.xlsx",
           "ad_sales": r"D:\anarix\data\ad_sales.xlsx"
    }

    # Read Excel and load into database
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
