from fastapi import APIRouter, Path
from typing import List, Union
from scripts.models.item import Item, ItemCreate, LoginRequest, ViewCart, CalculateTotalRequest
from scripts.handlers import item_handler
from app_constants.responses import ErrorResponses, SuccessResponse
from app_constants.constants import CommonConstants
from utils.log_module import logger

router = APIRouter()

@router.get("/users", response_model=dict)
def read_items():
    try:
        response = item_handler.read_items_logic()

        if response:
            return {
                CommonConstants.status: CommonConstants.success,
                CommonConstants.data: response,
                CommonConstants.message: SuccessResponse.users.format(user="User")  # Replace with actual user if needed
            }

        return {
            CommonConstants.status: CommonConstants.fail,
            CommonConstants.data: [],
            CommonConstants.message: ErrorResponses.users
        }

    except Exception as e:
        logger.exception(f"{ErrorResponses.users}: {e}")
        return {
            CommonConstants.status: CommonConstants.fail,
            CommonConstants.data: [],
            CommonConstants.message: str(e)
        }

@router.post("/items", response_model=dict)
def create_item(item: ItemCreate):
    try:
        created_item = item_handler.create_item_logic(item)
        return {
            CommonConstants.status: CommonConstants.success,
            CommonConstants.data: created_item,
            CommonConstants.message: SuccessResponse.create_item
        }
    except Exception as e:
        logger.exception(f"{ErrorResponses.create_item}: {e}")
        return {
            CommonConstants.status: CommonConstants.fail,
            CommonConstants.message: str(e)
        }

@router.delete("/items/{item_id}", response_model=dict)
def delete_item(item_id: int = Path(..., title="The ID of the item to delete")):
    try:
        result = item_handler.delete_item_logic(item_id)
        return {
            CommonConstants.status: CommonConstants.success,
            CommonConstants.data: result,
            CommonConstants.message: SuccessResponse.delete_item
        }
    except Exception as e:
        logger.exception(f"{ErrorResponses.delete_item}: {e}")
        return {
            CommonConstants.status: CommonConstants.fail,
            CommonConstants.message: str(e)
        }


@router.post("/login", response_model=dict)
def login_user(request: LoginRequest):
    try:
        result = item_handler.login_user_logic(request)

        if "error" in result:
            # If there's an error, handle the error and return a message
            return {
                CommonConstants.status: CommonConstants.fail,
                CommonConstants.message: result["error"],  # Top-level message for error
            }

        # For a successful login, the message goes outside of `data` and just contains user data
        return {
            CommonConstants.status: CommonConstants.success,
            CommonConstants.data: result["user"],  # Only send user data
            CommonConstants.message: SuccessResponse.login_success  # Message is outside data, only once
        }
    except Exception as e:
        logger.exception(f"{ErrorResponses.login_failed}: {e}")
        return {
            CommonConstants.status: CommonConstants.fail,
            CommonConstants.message: str(e)  # Top-level message for exception
        }

@router.get("/get_all_pizzas", response_model=dict)
def get_all_pizzas():
    try:
        response = item_handler.get_all_pizzas_logic()

        if response:
            return {
                CommonConstants.status: CommonConstants.success,
                CommonConstants.data: response,
                CommonConstants.message: SuccessResponse.pizzas_listing
            }

        return {
            CommonConstants.status: CommonConstants.fail,
            CommonConstants.data: [],
            CommonConstants.message: ErrorResponses.pizzas_listing
        }

    except Exception as e:
        logger.exception(f"{ErrorResponses.pizzas_listing}: {e}")
        return {
            CommonConstants.status: CommonConstants.fail,
            CommonConstants.data: [],
            CommonConstants.message: str(e)
        }


@router.post("/view_cart", response_model=dict)
def view_cart(request: ViewCart):
    try:
        # Get the cart data from the handler logic
        cart = item_handler.view_cart_logic(request.dict())

        if not cart["success"]:
            # Handle failure if the cart was not retrieved successfully
            return {
                "status": "fail",
                "message": cart.get("error", "Failed to retrieve cart details")
            }

        # Return the response with a clean structure
        return {
            "status": "success",
            "data": cart["data"],  # Just the cart data (list of pizzas inside 'pizzas')
            "message": "Cart viewed successfully"
        }

    except Exception as e:
        # Log the exception and return failure response
        logger.exception(f"Error viewing cart: {e}")
        return {
            "status": "fail",
            "message": str(e)
        }

@router.post("/calculate_total", response_model=dict)
def calculate_total(request: CalculateTotalRequest):
    try:
        total = item_handler.calculate_total_logic(request.items)
        return {
            CommonConstants.status: CommonConstants.success,
            CommonConstants.data: total['data'],  # Flatten the data if needed
            CommonConstants.message: SuccessResponse.calculate_total
        }
    except Exception as e:
        logger.exception(f"{ErrorResponses.calculate_total_failed}: {e}")
        return {
            CommonConstants.status: CommonConstants.fail,
            CommonConstants.message: str(e)
        }