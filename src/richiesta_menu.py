from datetime import date
from typing import List, Optional
from fastapi import Query
from src.piatto_manuale import PiattoManuale
from src.enums import GIORNI_LAVORATIVI_DEFAULT, Giorni_settimana, Stagione

class Richiesta:
    def __init__(
        self,
        stagioni: Optional[List[Stagione]] = Query(None),
        tempo_massimo: Optional[int] = 1000,
        data_inizio_settimana : Optional[date] = None,
        giorni_lavorativi : Optional[List[Giorni_settimana]] = GIORNI_LAVORATIVI_DEFAULT,
        pasti_bloccati : Optional[List[PiattoManuale]] = None
    ):
        self.stagioni = stagioni
        self.tempo_massimo = tempo_massimo
        self.data_inizio_settimana = data_inizio_settimana
        self.giorni_lavorativi = giorni_lavorativi
        self.pasti_bloccati = pasti_bloccati