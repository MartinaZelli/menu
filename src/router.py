from fastapi import APIRouter
from src.risposta_menu import Risposta
import src.service
from src.richiesta_menu import Richiesta

router = APIRouter(
    prefix="/menu",
    tags=["menu"]
)

@router.post("") 
async def genera_menu(richiesta: Richiesta) -> Risposta: 
    # La logica ora è interamente gestita dentro genera_menu_ordinato
    # che apre e chiude la connessione al database autonomamente
    risultato = src.service.genera_menu_ordinato(richiesta)
    return risultato