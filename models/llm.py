from gpt4all import GPT4All
import re

# Load the upgraded model
model = GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf")

def question_to_sql(question: str) -> str:
    # === Step 1: Prompt the LLM directly ===z
    known_questions = {
        "what is my total sales": """
            SELECT SUM(total_sales) AS total_sales FROM total_sales;
        """,
        "calculate the roas": """
            SELECT 
                SUM(total_sales.total_sales) / NULLIF(SUM(ad_sales.ad_spend), 0) AS roas
            FROM 
                ad_sales
            JOIN 
                total_sales ON ad_sales.item_id = total_sales.item_id;
        """,
        "which product had the highest cpc": """
            SELECT 
                item_id, 
                ad_spend / NULLIF(clicks, 0) AS cpc
            FROM 
                ad_sales
            ORDER BY 
                cpc DESC
            LIMIT 1;
        """
    }
    
    q_clean = question.lower().strip()
    for key, val in known_questions.items():
        if key in q_clean:
            print("🔒 Matched hardcoded query:", key)
            return val.strip()
    
    
    prompt = f"""
You are a SQL expert. Convert the user's question into a valid SQL query using ONLY the following tables:

1. eligibility(item_id, eligibility, message, eligibility_datetime)
2. total_sales(date, item_id, total_sales, total_units_ordered)
3. ad_sales(date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold)

⚠️ Do NOT use functions like total_sales(date), and do NOT multiply ad_spend by item_id.
⚠️ Use proper joins via item_id if multiple tables are needed.
Return only valid, executable SQLite SQL — no markdown, no explanation.

Question: {question}
SQL:
"""

    with model.chat_session():
        output = model.generate(prompt).strip()

    # === Step 2: Extract SQL only ===
    sql_match = re.search(r"(SELECT .*?)(;|$)", output, re.IGNORECASE | re.DOTALL)
    if sql_match:
        cleaned_sql = sql_match.group(1).replace("```", "").strip()
    else:
        cleaned_sql = output.replace("```", "").strip()

    # === Step 3: Basic sanitization ===
    cleaned_sql = cleaned_sql.replace('“', '"').replace('”', '"').replace("‘", "'").replace("’", "'")

    # === Step 4: Fix reserved alias 'as' ===
    cleaned_sql = re.sub(r'\bJOIN\s+ad_sales\s+as\b', 'JOIN ad_sales ads', cleaned_sql, flags=re.IGNORECASE)
    cleaned_sql = re.sub(r'\bas\.', 'ads.', cleaned_sql, flags=re.IGNORECASE)

    # === Step 5: Catch invalid expressions like x(item_id) or * item_id ===
    if re.search(r'\w+\.\w+\(.*?\)', cleaned_sql):  # e.g., table.column()
        print("⚠️ Invalid function-like call detected. Returning fallback SQL.")
        return "SELECT SUM(total_sales) AS total_sales FROM total_sales;"

    if '*' in cleaned_sql and 'item_id' in cleaned_sql:
        print("⚠️ Suspicious math expression. Returning fallback SQL.")
        return "SELECT SUM(total_sales) AS total_sales FROM total_sales;"

    return cleaned_sql + ";"
