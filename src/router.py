from typing import List

from fastapi import APIRouter, Depends, FastAPI
from pydantic import BaseModel

import src.service
from src.richiesta_menu import Richiesta
from src.enums import Proteina, Stagione, Tipologia
from src.piatto import Piatto

router = APIRouter(
    prefix="/menu",
    tags=["menu"]
)

db = src.service.db

@router.get("")
async def mostra_piatti(filtro: Richiesta = Depends())->List[Piatto]:
    risultato = db
    if filtro.stagioni:
        risultato = [p for p in risultato if p.stagione in filtro.stagioni  ]
    if filtro.tempo_massimo:
        risultato = [p for p in risultato if p.tempo <= filtro.tempo_massimo]
    
    return risultato
   

