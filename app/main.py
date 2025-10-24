from fastapi import FastAPI
# Asegúrate de que todos los routers estén importados
from .routers import client_auth, client_menu, client_cart

app = FastAPI(
    title="API para App de Restaurante",
    version="1.0.0"
)

# --- CORRECCIÓN ---
# Incluir TODOS los routers en la aplicación principal
app.include_router(client_auth.router)
app.include_router(client_menu.router)
app.include_router(client_cart.router)

@app.get("/", tags=["Root"])
def read_root():
    """Punto de entrada principal de la API."""
    return {"message": "Bienvenido a la API del Restaurante"}
