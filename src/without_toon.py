import sqlite3
import json
from ollama import Client

# --- Configuration ---
DB_NAME = 'users.db'
OLLAMA_MODEL = 'deepseek-r1:1.5b'  # Replace with a model you have pulled

def fetch_data_as_json(query: str) -> str:
    """Run an SQLite query and return results as pretty JSON."""
    conn = None
    data_list = []
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            data_list.append(dict(row))
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return json.dumps({"error": f"Database error occurred: {e}"})
    finally:
        if conn:
            conn.close()

    return json.dumps(data_list, indent=2)

def query_ollama_with_data(user_question: str, db_json_data: str) -> str:
    """Send question + JSON context to Ollama and return the response object."""
    ollama_client = Client(host='http://localhost:11434')

    system_prompt = (
        "You are an intelligent, helpful data assistant. Your task is to answer the user's "
        "question based ONLY on the context provided in the JSON data below. "
        "Do not use any external knowledge. If the JSON context is empty or does not contain the answer, say you could not find the information."
    )

    user_prompt = (
        f"USER QUESTION: {user_question}\n\n"
        f"CONTEXTUAL JSON DATA:\n---\n{db_json_data}\n---"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    print(f"🧠 Sending request to Ollama with model: {OLLAMA_MODEL}...")
    try:
        response = ollama_client.chat(model=OLLAMA_MODEL, messages=messages)
        return response
    except Exception as e:
        return f"Ollama API Error: {e}. Is Ollama running and is the model '{OLLAMA_MODEL}' pulled?"


if __name__ == '__main__':
    sql_query = """
    SELECT name, age, fav_food, city
    FROM users
    WHERE age > 18;
    """

    llm_question = "Please list the names, ages, and cities of all users who are older than 18"

    json_data = fetch_data_as_json(sql_query)
    if "error" in json_data.lower():
        print(json_data)
    else:
        final_answer = query_ollama_with_data(llm_question, json_data)
        try:
            print(final_answer['message']['content'])
        except Exception:
            print(final_answer)
