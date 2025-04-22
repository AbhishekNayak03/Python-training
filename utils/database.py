# database.py
import psycopg2
from psycopg2 import sql
from typing import List, Dict, Any
import base64

# Database connection parameters
DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "postgres"

# Function to get a connection to the database
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None


# Function to fetch all items from the database (generic)
def fetch_items_from_db() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    if conn is None:
        return {"error": "Database connection failed."}

    try:
        cur = conn.cursor()
        query = sql.SQL("SELECT id, name, email FROM users")
        cur.execute(query)
        rows = cur.fetchall()
        users = [{"id": row[0], "name": row[1], "email": row[2]} for row in rows]
        cur.close()
        conn.close()
        return users
    except Exception as e:
        return {"error": f"Error fetching items: {e}"}

def insert_item_into_db(name: str, email: str) -> dict:
    try:
        conn = psycopg2.connect(
            host="localhost",
            dbname="postgres",
            user="postgres",
            password="postgres"
        )
        cur = conn.cursor()
        query = sql.SQL("INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id")
        cur.execute(query, (name, email))
        item_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return {"id": item_id, "name": name, "email": email}
    except Exception as e:
        return {"error": str(e)}

def delete_item_from_db(item_id: int) -> dict:
    try:
        conn = psycopg2.connect(
            host="localhost",
            dbname="postgres",
            user="postgres",
            password="postgres"
        )
        cur = conn.cursor()
        query = sql.SQL("DELETE FROM users WHERE id = %s RETURNING id")
        cur.execute(query, (item_id,))
        deleted = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        if deleted:
            return {"message": f"Item with id {item_id} deleted successfully."}
        else:
            return {"error": f"Item with id {item_id} not found."}
    except Exception as e:
        return {"error": str(e)}


def login_user(email: str, password: str) -> dict:
    try:
        # Decode the base64-encoded password
        decoded_password = base64.b64decode(password).decode('utf-8')

        conn = psycopg2.connect(
            host="localhost",
            dbname="postgres",
            user="postgres",
            password="postgres"
        )
        cur = conn.cursor()

        # Query to match email & decoded password
        query = sql.SQL("SELECT id, name, email FROM users WHERE email = %s AND password = %s")
        cur.execute(query, (email, decoded_password))
        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
            return {
                "user": {
                    "id": user[0],
                    "name": user[1],
                    "email": user[2]
                }
            }
        else:
            return {"error": "Invalid email or password."}

    except Exception as e:
        return {"error": str(e)}

def get_all_pizzas_from_db() -> dict:
    try:
        conn = psycopg2.connect(
            host="localhost",
            dbname="postgres",
            user="postgres",
            password="postgres"
        )
        cur = conn.cursor()

        query = sql.SQL("SELECT pizza_id, name, price FROM pizzas")
        cur.execute(query)
        rows = cur.fetchall()

        cur.close()
        conn.close()

        pizzas = [
            {"pizza_id": row[0], "name": row[1], "price": float(row[2])}
            for row in rows
        ]

        return {"pizzas": pizzas}

    except Exception as e:
        return {"error": str(e)}

def view_cart_details_from_db(pizza_ids: list) -> dict:
    if not pizza_ids:
        return {"error": "No pizza_ids provided"}

    try:
        conn = psycopg2.connect(
            host="localhost",
            dbname="postgres",
            user="postgres",
            password="postgres"
        )
        cur = conn.cursor()

        # Prepare dynamic query with IN clause
        query = sql.SQL("""
            SELECT pizza_id, name, price, ingredients, description
            FROM pizzas
            WHERE pizza_id = ANY(%s)
        """)

        cur.execute(query, (pizza_ids,))
        rows = cur.fetchall()

        cur.close()
        conn.close()

        pizzas = [
            {
                "pizza_id": row[0],
                "name": row[1],
                "price": float(row[2]),
                "ingredients": row[3],
                "description": row[4]
            }
            for row in rows
        ]

        return {"success": True, "data": pizzas}

    except Exception as e:
        return {"success": False, "error": str(e)}