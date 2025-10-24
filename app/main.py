from fastapi import FastAPI
from .routers import client_auth, client_menu, client_cart, admin_auth, client_orders

app = FastAPI(
    title="API para App de Restaurante",
    version="1.0.0"
)

app.include_router(client_auth.router)
app.include_router(client_menu.router)
app.include_router(client_cart.router)
app.include_router(admin_auth.router)
app.include_router(client_orders.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido a la API del Restaurante"}
