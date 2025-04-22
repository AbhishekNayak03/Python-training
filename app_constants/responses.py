class ErrorResponses:
    users: str = "Failed to list users"
    create_user: str = "Failed to create user"
    delete_item: str = "Failed to delete item"
    login_failed: str = "Login failed"
    pizzas_listing: str = "Failed to list pizzas"
    cart_view_failed: str = "Failed to view cart"
    calculate_total_failed: str = "Failed to calculate total"

class SuccessResponse:
    users: str = "Successfully listed users"
    create_user: str = "Sign-up successful!"
    delete_item: str = "Successfully deleted item"
    login_success: str = "Login successful!"
    pizzas_listing: str = "Successfully listed all pizzas"
    cart_view: str = "Successfully retrieved cart"
    calculate_total: str = "Successfully calculated total"