from typing import List

from fastapi import APIRouter, Depends, FastAPI
from pydantic import BaseModel

from src.risposta_menu import Risposta
import src.service
from src.richiesta_menu import Richiesta
from src.enums import Proteina, Stagione, Tipologia
from src.piatto import Piatto

router = APIRouter(
    prefix="/menu",
    tags=["menu"]
)

db = src.service.db
frequenza_macro = src.service.frequenza_macro

@router.get("")
async def mostra_piatti(richiesta: Richiesta = Depends())->Risposta:
    risultato = src.service.genera_menu_ordinato(richiesta)
    
    
    return risultato
   

