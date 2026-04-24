from fastapi import APIRouter, HTTPException
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

@router.post("/salva")
async def salva_menu(risposta: Risposta):
    successo = src.service.salva_menu_settimanale(risposta)
    if not successo:
        raise HTTPException(status_code=500, detail="Errore nel salvataggio del menu")
    return {"status": "success", "message": "Menu salvato con successo"}