from flask import Flask, request, render_template
from models.llm import question_to_sql
from utils.query_executor import execute_sql
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

def generate_chart(result, columns):
    try:
        if not result or not columns:
            return None

        # Find first numeric column
        numeric_col_idx = [i for i, col in enumerate(zip(*result)) if all(isinstance(x, (int, float)) for x in col)]
        if not numeric_col_idx:
            return None

        x = [str(row[0]) for row in result]
        y = [row[numeric_col_idx[0]] for row in result]

        plt.figure(figsize=(6, 4))
        plt.bar(x, y, color="skyblue")
        plt.xlabel(columns[0])
        plt.ylabel(columns[numeric_col_idx[0]])
        plt.title("Generated Chart")
        plt.xticks(rotation=45)
        plt.tight_layout()

        chart_filename = "chart.png"
        chart_path = os.path.join("static", chart_filename)
        plt.savefig(chart_path)
        plt.close()

        return chart_filename  # Just return filename, not full path
    except Exception as e:
        print("⚠️ Chart Error:", e)
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    sql = ""
    result = []
    columns = []
    table_html = ""
    chart_filename = None

    if request.method == "POST":
        question = request.form.get("question", "")
        try:
            sql = question_to_sql(question)
            result, columns = execute_sql(sql)

            if result and columns:
                table_html = render_table(result, columns)

            chart_filename = generate_chart(result, columns)

        except Exception as e:
            table_html = f"<p class='text-danger'>Error: {e}</p>"

    return render_template("index.html", sql=sql, table=table_html, chart=chart_filename)

def render_table(result, columns):
    html = "<table class='table table-bordered table-striped'><thead><tr>"
    html += "".join(f"<th>{col}</th>" for col in columns)
    html += "</tr></thead><tbody>"
    for row in result:
        html += "<tr>" + "".join(f"<td>{val}</td>" for val in row) + "</tr>"
    html += "</tbody></table>"
    return html

if __name__ == "__main__":
    app.run(debug=True)
