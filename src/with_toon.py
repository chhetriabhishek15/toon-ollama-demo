import sqlite3
import json
from ollama import Client 
from toon_format import encode

# --- Configuration ---
DB_NAME = 'users.db'
OLLAMA_MODEL = 'deepseek-r1:1.5b'  # Replace with a model you have pulled

def fetch_data_as_toon(query: str) -> str:
    """Run an SQLite query and return results encoded with TOON."""
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

    # Encode using the project's TOON encoder for compact context
    return encode(data_list)

def query_ollama_with_data(user_question: str, db_toon_data: str) -> str:
    """Send question + TOON context to Ollama and return the response object."""
    ollama_client = Client(host='http://localhost:11434')

    system_prompt = (
        "You are an intelligent, helpful data assistant. Your task is to answer the user's "
        "question based ONLY on the context provided in the TOON data below. "
        "Do not use any external knowledge. If the TOON context is empty or does not contain the answer, say you could not find the information."
    )

    user_prompt = (
        f"USER QUESTION: {user_question}\n\n"
        f"CONTEXTUAL TOON DATA:\n---\n{db_toon_data}\n---"
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

    toon_data = fetch_data_as_toon(sql_query)
    if "error" in toon_data.lower():
        print(toon_data)
    else:
        final_answer = query_ollama_with_data(llm_question, toon_data)
        try:
            print(final_answer['message']['content'])
        except Exception:
            print(final_answer)
