# AI SQL Assistant with LLMs

This project lets you ask natural language questions and converts them into SQL queries using a local language model (GPT4All). It uses Flask for the web interface and supports data visualization with Matplotlib.

## Features
- Converts questions into SQL queries using LLM
- Executes queries on SQLite
- Displays results and graphs on a web UI

## Technologies
- Python, Flask
- GPT4All (Mistral model)
- SQLite, Matplotlib

## Setup Instructions
1. Install dependencies:  
   `pip install -r requirements.txt`
2. Load your Excel datasets into SQLite using `load_data.py`
3. Run the app:  
   `python flask_app.py`
4. Open [http://127.0.0.1:5000](http://127.0.0.1:5000)



