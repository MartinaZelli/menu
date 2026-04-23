import random
from datetime import date
from typing import List, Dict, Optional
from sqlalchemy.orm import Session

from src.database import SessionLocal, PiattoDB, MacroDB
from src.risposta_menu import Pasti, Pasti_settimana, Risposta
from src.piatto import Piatto
from src.enums import Giorni_settimana, Proteina, Stagione, Tipologia
from src.richiesta_menu import Richiesta

def genera_pool_proteine_garantito(frequenza: Dict[str, int], totale_target: int) -> List[str]:
    """Mantiene la logica originale: garantisce almeno una volta ogni proteina richiesta e completa il pool."""
    proteine_richieste = [p for p, qta in frequenza.items() if qta > 0]
    pool_finale = list(proteine_richieste)
    
    rimanenti_pool = []
    for p, qta in frequenza.items():
        istanze_extra = qta - 1
        if istanze_extra > 0:
            rimanenti_pool.extend([p] * istanze_extra)
    
    posti_da_riempire = totale_target - len(pool_finale)
    if posti_da_riempire > 0:
        k_da_estrarre = min(posti_da_riempire, len(rimanenti_pool))
        extra_estratti = random.sample(rimanenti_pool, k=k_da_estrarre)
        pool_finale.extend(extra_estratti)
    
    random.shuffle(pool_finale)
    return pool_finale

def seleziona_piatto_da_db(
    proteina_target: str, 
    vincolo_lavoro: bool, 
    pool_piatti_db: List[PiattoDB],
    piatti_gia_usati: List[int]
) -> Optional[Piatto]:
    """Seleziona un piatto dal database convertendolo nel modello Pydantic."""
    # Filtro per proteina e duplicati
    candidati = [p for p in pool_piatti_db if p.proteina == proteina_target and p.id not in piatti_gia_usati]
    
    # Se finiti i piatti nuovi per quella proteina, ripeschiamo dai già usati
    if not candidati:
        candidati = [p for p in pool_piatti_db if p.proteina == proteina_target]

    if vincolo_lavoro:
        candidati_lavoro = [p for p in candidati if p.adatto_al_lavoro]
        if candidati_lavoro:
            candidati = candidati_lavoro

    if not candidati:
        return None
        
    scelto = random.choice(candidati)
    return Piatto(
        id=scelto.id,
        nome=scelto.nome,
        proteina=Proteina(scelto.proteina),
        stagione=Stagione(scelto.stagione),
        tempo=scelto.tempo,
        adatto_al_lavoro=scelto.adatto_al_lavoro,
        tipologia=Tipologia(scelto.tipologia)
    )

def genera_menu_ordinato(richiesta: Richiesta) -> Risposta:
    db_session = SessionLocal()
    try:
        # 1. CARICAMENTO REGOLE E PIATTI DAL DB
        macro_db = db_session.query(MacroDB).all()
        frequenza_ideale = {m.proteina: m.frequenza for m in macro_db}

        query = db_session.query(PiattoDB)
        if richiesta.stagioni:
            stagioni_val = [s.value for s in richiesta.stagioni]
            query = query.filter(PiattoDB.stagione.in_(stagioni_val + ["generico"]))
        
        if richiesta.tempo_massimo:
            query = query.filter(PiattoDB.tempo <= richiesta.tempo_massimo)
        
        db_filtrato = query.all()

        # 2. GESTIONE PASTI BLOCCATI E CALCOLO RESIDUO
        pasti_bloccati = richiesta.pasti_bloccati or []
        mappa_bloccati = {f"{pb.giorno}_{pb.momento}": pb.piatto for pb in pasti_bloccati}
        
        frequenza_residua = frequenza_ideale.copy()
        piatti_usati_ids = []

        for pb in pasti_bloccati:
            piatti_usati_ids.append(pb.piatto.id)
            prot = pb.piatto.proteina.value if hasattr(pb.piatto.proteina, 'value') else pb.piatto.proteina
            if prot in frequenza_residua:
                frequenza_residua[prot] = max(0, frequenza_residua[prot] - 1)

        # 3. GENERAZIONE POOL PROTEINE PER GLI SLOT VUOTI
        posti_liberi = 14 - len(pasti_bloccati)
        pool_proteine = genera_pool_proteine_garantito(frequenza_residua, posti_liberi)
        it_pool = iter(pool_proteine)

        # 4. COSTRUZIONE SETTIMANA
        risultati_giornalieri = {}
        piatto_vuoto = Piatto(id=0, nome="Nessun match", tempo=0, adatto_al_lavoro=False)
        ordine_giorni = ["lunedi", "martedi", "mercoledi", "giovedi", "venerdi", "sabato", "domenica"]

        for nome_giorno in ordine_giorni:
            enum_giorno = Giorni_settimana[nome_giorno.upper()]
            is_lavorativo = enum_giorno in richiesta.giorni_lavorativi
            pasti_del_giorno = {"pranzo": [], "cena": []}

            for momento in ["pranzo", "cena"]:
                chiave = f"{nome_giorno}_{momento}"
                
                if chiave in mappa_bloccati:
                    pasti_del_giorno[momento] = [mappa_bloccati[chiave]]
                else:
                    prot_target = next(it_pool, None)
                    if prot_target:
                        piatto = seleziona_piatto_da_db(
                            prot_target, 
                            (momento == "pranzo" and is_lavorativo), 
                            db_filtrato, 
                            piatti_usati_ids
                        )
                        if piatto:
                            pasti_del_giorno[momento] = [piatto]
                            piatti_usati_ids.append(piatto.id)
                        else:
                            pasti_del_giorno[momento] = [piatto_vuoto]
                    else:
                        pasti_del_giorno[momento] = [piatto_vuoto]

            risultati_giornalieri[nome_giorno] = Pasti(
                pranzo=pasti_del_giorno["pranzo"],
                cena=pasti_del_giorno["cena"]
            )

        # 5. RISPOSTA FINALE
        dt_inizio = richiesta.data_inizio_settimana or date.today()
        giorno_sett_inizio = list(Giorni_settimana)[dt_inizio.weekday()]

        return Risposta(
            giorno_inizio_settimana=giorno_sett_inizio,
            data_inizio_settimana=dt_inizio,
            tabella=Pasti_settimana(**risultati_giornalieri)
        )
    finally:
        db_session.close()