import sqlite3

def execute_sql(sql: str):
    try:
        conn = sqlite3.connect("db/ecommerce.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]  # ✅ get column names
        conn.close()
        return rows, columns  # ✅ return both rows and columns
    except Exception as e:
        return [], [str(e)]  # fallback if there's an error
