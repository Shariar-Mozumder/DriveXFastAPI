from fastapi import FastAPI
from sqlalchemy_orm.db_config import metadata, engine
from auth_management import auth_router
from product_management import product_router
# from category_management import category_router
# # from admin_management import admin_router
# from order_cart_management import order_cart_router
# from auction_management import auction_router
import uvicorn

# Create database tables on application startup
metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI()

# Include your routers
app.include_router(auth_router, prefix="/auths", tags=["Auths"])
app.include_router(product_router, prefix="/products", tags=["Products"])
# app.include_router(category_router, prefix="/categories", tags=["Categories"])
# # app.include_router(admin_router, prefix="/admins", tags=["Admins"])
# app.include_router(auction_router, prefix="/auctions", tags=["Auctions"])
# app.include_router(order_cart_router, prefix="/order_carts", tags=["Order_carts"])

# Example health check endpoint (optional)
@app.get("/health")
def health_check():
    return {"status": "Application is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
