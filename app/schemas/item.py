from pydantic import BaseModel
from typing import List, Optional

# Esquema base para un platillo, con los campos comunes
class ItemBase(BaseModel):
    name: str
    shortDescription: Optional[str] = None
    price: float
    imageUrl: Optional[str] = None

# Esquema para la respuesta al obtener una lista de platillos
class Item(ItemBase):
    id: str # En la BBDD es UUID, pero lo manejamos como string en la API

    class Config:
        from_attributes = True # Permite que Pydantic lea los datos desde el modelo de SQLAlchemy

# Esquema detallado de un platillo, como en tu API contract
class ItemDetail(Item):
    longDescription: Optional[str] = None
    # Nota: Tu BBDD no tiene 'customizationOptions'. Necesitarías añadir una tabla para esto.
    # customizationOptions: List = []