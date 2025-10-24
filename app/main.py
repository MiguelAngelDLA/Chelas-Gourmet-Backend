from fastapi import FastAPI

from app.routers import client_auth, client_menu

app = FastAPI(
    title="API para App de Restaurante",
    version="1.0.0"
)

app.include_router(client_auth.router)
app.include_router(client_menu.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido a la API del Restaurante"}