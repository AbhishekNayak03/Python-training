# handlers/item_handler.py
from utils.database import fetch_items_from_db, insert_item_into_db, delete_item_from_db, login_user,get_all_pizzas_from_db, view_cart_details_from_db
from scripts.models.item import Item, ItemCreate, LoginRequest
from utils.log_module import logger
from typing import List, Union

def read_items_logic() -> Union[List[Item], dict]:
    logger.info("Reading items from DB")
    raw_items = fetch_items_from_db()
    if isinstance(raw_items, list):
        return [Item(id=item["id"], name=item["name"], email=item["email"]) for item in raw_items]
    else:
        return {"error": "Failed to fetch items"}

def create_item_logic(item: ItemCreate) -> dict:
    logger.info(f"Creating item: {item}")
    return insert_item_into_db(item.name, item.email)

def delete_item_logic(item_id: int) -> dict:
    logger.info(f"Deleting item with id: {item_id}")
    return delete_item_from_db(item_id)

def get_all_pizzas_logic() -> dict:
    logger.info("Fetching all pizzas")
    return get_all_pizzas_from_db()


def view_cart_logic(payload: dict) -> dict:
    logger.info("Fetching cart details")

    # Get pizza_ids from payload (instead of items)
    pizza_ids = payload.get("pizza_ids")

    if not pizza_ids or not isinstance(pizza_ids, list):
        return {"success": False, "error": "Missing or invalid 'pizza_ids' in payload"}

    # If quantities are part of the request, we can handle them too. Default to 1 if missing.
    quantities = {pizza_id: 1 for pizza_id in pizza_ids}  # Default to quantity 1 for all pizzas

    # Fetch pizza details from the database
    pizzas = view_cart_details_from_db(pizza_ids)

    # Attach quantity information to the pizzas
    if pizzas["success"]:
        for pizza in pizzas["data"]:
            pizza["quantity"] = quantities.get(pizza["pizza_id"], 1)  # Default quantity to 1

    return pizzas


def login_user_logic(request: LoginRequest) -> dict:
    logger.info(f"Attempting login for email: {request.email}")
    user = login_user(request.email, request.password)

    if "error" in user:
        return {"error": user["error"]}

    if user:
        return {
            "message": "Login successful!",
            "user": user
        }
    else:
        return {"error": "Invalid email or password."}
