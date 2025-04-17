# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scripts.services.item_service import router as item_router
import uvicorn

app = FastAPI()

# Include the item routes
app.include_router(item_router)
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "DELETE"],
        allow_headers=["*"],
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
