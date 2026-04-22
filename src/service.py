from datetime import date
import random
from typing import Dict, List, Optional

from src.risposta_menu import Pasti, Pasti_settimana, Risposta
from src.piatto import Piatto
from src.enums import Giorni_settimana, Proteina, Stagione, Tipologia
from src.richiesta_menu import Richiesta

frequenza_macro : Dict[Proteina, int] = {
    Proteina.LEGUMI: 3,        # Es: Lunedì pranzo, Mercoledì cena, Venerdì pranzo
    Proteina.LATTICINI: 4,     # Es: Martedì cena, Sabato pranzo
    Proteina.CARNE_BIANCA: 4,  # Es: Lunedì cena, Giovedì pranzo, Sabato cena
    Proteina.CARNE_ROSSA: 1,   # Es: Domenica pranzo
    Proteina.PESCE: 3,         # Es: Martedì pranzo, Venerdì cena, Domenica cena
    Proteina.UOVA: 3           # Es: Mercoledì pranzo, Giovedì cena
}

db: List[Piatto] = [
    # --- LATTICINI (6 piatti) ---
    Piatto(id=1, nome="Pasta al pomodoro e mozzarella", tempo=30, adatto_al_lavoro=False, proteina=Proteina.LATTICINI, tipologia=Tipologia.PRIMO),
    Piatto(id=2, nome="Tomino alla piastra", tempo=5, adatto_al_lavoro=True, proteina=Proteina.LATTICINI, tipologia=Tipologia.SECONDO),
    Piatto(id=12, nome="Insalata greca", tempo=10, adatto_al_lavoro=True, proteina=Proteina.LATTICINI, tipologia=Tipologia.UNICO, stagione=Stagione.ESTATE),
    Piatto(id=20, nome="Gnocchi al gorgonzola", tempo=15, adatto_al_lavoro=False, proteina=Proteina.LATTICINI, tipologia=Tipologia.PRIMO, stagione=Stagione.INVERNO),
    Piatto(id=22, nome="Pasta fredda tricolore", tempo=20, adatto_al_lavoro=True, proteina=Proteina.LATTICINI, tipologia=Tipologia.PRIMO, stagione=Stagione.ESTATE),
    Piatto(id=31, nome="Ricotta fresca e miele", tempo=5, adatto_al_lavoro=True, proteina=Proteina.LATTICINI, tipologia=Tipologia.SECONDO, stagione=Stagione.ESTATE),

    # --- LEGUMI (9 piatti) ---
    Piatto(id=3, nome="Minestrone di verdure", tempo=40, adatto_al_lavoro=False, proteina=Proteina.LEGUMI, tipologia=Tipologia.PRIMO, stagione=Stagione.INVERNO),
    Piatto(id=5, nome="Insalata di ceci e tonno", tempo=10, adatto_al_lavoro=True, proteina=Proteina.LEGUMI, tipologia=Tipologia.UNICO, stagione=Stagione.ESTATE),
    Piatto(id=11, nome="Lenticchie in umido", tempo=45, adatto_al_lavoro=True, proteina=Proteina.LEGUMI, tipologia=Tipologia.SECONDO, stagione=Stagione.INVERNO),
    Piatto(id=16, nome="Polpette di soia", tempo=20, adatto_al_lavoro=True, proteina=Proteina.LEGUMI, tipologia=Tipologia.SECONDO),
    Piatto(id=17, nome="Quinoa con verdure", tempo=25, adatto_al_lavoro=True, proteina=Proteina.LEGUMI, tipologia=Tipologia.UNICO),
    Piatto(id=23, nome="Fagioli all'uccelletto", tempo=30, adatto_al_lavoro=True, proteina=Proteina.LEGUMI, tipologia=Tipologia.CONTORNO),
    Piatto(id=28, nome="Hummus con cruditè", tempo=15, adatto_al_lavoro=True, proteina=Proteina.LEGUMI, tipologia=Tipologia.UNICO),
    Piatto(id=30, nome="Zuppa di farro e lenticchie", tempo=40, adatto_al_lavoro=True, proteina=Proteina.LEGUMI, tipologia=Tipologia.UNICO, stagione=Stagione.INVERNO),
    Piatto(id=32, nome="Zuppa di piselli freschi", tempo=30, adatto_al_lavoro=False, proteina=Proteina.LEGUMI, tipologia=Tipologia.PRIMO, stagione=Stagione.MEZZA),

    # --- CARNE BIANCA (7 piatti) ---
    Piatto(id=4, nome="Hamburger di pollo", tempo=10, adatto_al_lavoro=True, proteina=Proteina.CARNE_BIANCA, tipologia=Tipologia.SECONDO),
    Piatto(id=19, nome="Spiedini di tacchino", tempo=15, adatto_al_lavoro=True, proteina=Proteina.CARNE_BIANCA, tipologia=Tipologia.SECONDO),
    Piatto(id=27, nome="Scaloppine al limone", tempo=15, adatto_al_lavoro=True, proteina=Proteina.CARNE_BIANCA, tipologia=Tipologia.SECONDO),
    Piatto(id=33, nome="Insalata di pollo e mele", tempo=15, adatto_al_lavoro=True, proteina=Proteina.CARNE_BIANCA, tipologia=Tipologia.UNICO, stagione=Stagione.ESTATE),
    Piatto(id=34, nome="Pollo al curry", tempo=25, adatto_al_lavoro=True, proteina=Proteina.CARNE_BIANCA, tipologia=Tipologia.SECONDO, stagione=Stagione.INVERNO),
    Piatto(id=35, nome="Tacchino alle erbe", tempo=15, adatto_al_lavoro=True, proteina=Proteina.CARNE_BIANCA, tipologia=Tipologia.SECONDO, stagione=Stagione.MEZZA),
    Piatto(id=44, nome="Bocconcini di pollo ai funghi", tempo=20, adatto_al_lavoro=True, proteina=Proteina.CARNE_BIANCA, tipologia=Tipologia.SECONDO, stagione=Stagione.INVERNO),

    # --- CARNE ROSSA (6 piatti) ---
    Piatto(id=10, nome="Spezzatino di manzo", tempo=90, adatto_al_lavoro=False, proteina=Proteina.CARNE_ROSSA, tipologia=Tipologia.SECONDO, stagione=Stagione.INVERNO),
    Piatto(id=13, nome="Straccetti di vitello", tempo=10, adatto_al_lavoro=True, proteina=Proteina.CARNE_ROSSA, tipologia=Tipologia.SECONDO),
    Piatto(id=24, nome="Bistecca ai ferri", tempo=8, adatto_al_lavoro=False, proteina=Proteina.CARNE_ROSSA, tipologia=Tipologia.SECONDO),
    Piatto(id=36, nome="Polpette al sugo", tempo=35, adatto_al_lavoro=False, proteina=Proteina.CARNE_ROSSA, tipologia=Tipologia.SECONDO, stagione=Stagione.INVERNO),
    Piatto(id=37, nome="Carpaccio di bresaola", tempo=5, adatto_al_lavoro=True, proteina=Proteina.CARNE_ROSSA, tipologia=Tipologia.SECONDO, stagione=Stagione.ESTATE),
    Piatto(id=45, nome="Tagliata di manzo e rucola", tempo=12, adatto_al_lavoro=False, proteina=Proteina.CARNE_ROSSA, tipologia=Tipologia.SECONDO, stagione=Stagione.MEZZA),

    # --- PESCE (7 piatti) ---
    Piatto(id=8, nome="Salmone al vapore", tempo=15, adatto_al_lavoro=True, proteina=Proteina.PESCE, tipologia=Tipologia.SECONDO),
    Piatto(id=15, nome="Baccalà alla livornese", tempo=40, adatto_al_lavoro=False, proteina=Proteina.PESCE, tipologia=Tipologia.SECONDO),
    Piatto(id=21, nome="Branzino al sale", tempo=35, adatto_al_lavoro=False, proteina=Proteina.PESCE, tipologia=Tipologia.SECONDO),
    Piatto(id=26, nome="Cous cous di pesce", tempo=30, adatto_al_lavoro=True, proteina=Proteina.PESCE, tipologia=Tipologia.UNICO, stagione=Stagione.ESTATE),
    Piatto(id=38, nome="Sogliola alla mugnaia", tempo=10, adatto_al_lavoro=True, proteina=Proteina.PESCE, tipologia=Tipologia.SECONDO, stagione=Stagione.MEZZA),
    Piatto(id=39, nome="Zuppa di pesce", tempo=50, adatto_al_lavoro=False, proteina=Proteina.PESCE, tipologia=Tipologia.UNICO, stagione=Stagione.INVERNO),
    Piatto(id=46, nome="Filetto di orata al forno", tempo=20, adatto_al_lavoro=False, proteina=Proteina.PESCE, tipologia=Tipologia.SECONDO),

    # --- UOVA (7 piatti) ---
    Piatto(id=7, nome="Frittata alle erbe", tempo=15, adatto_al_lavoro=True, proteina=Proteina.UOVA, tipologia=Tipologia.SECONDO),
    Piatto(id=9, nome="Pasta alla carbonara", tempo=20, adatto_al_lavoro=False, proteina=Proteina.UOVA, tipologia=Tipologia.PRIMO),
    Piatto(id=18, nome="Uova in purgatorio", tempo=15, adatto_al_lavoro=False, proteina=Proteina.UOVA, tipologia=Tipologia.SECONDO),
    Piatto(id=29, nome="Omelette al formaggio", tempo=10, adatto_al_lavoro=False, proteina=Proteina.UOVA, tipologia=Tipologia.SECONDO),
    Piatto(id=40, nome="Uova sode e asparagi", tempo=15, adatto_al_lavoro=True, proteina=Proteina.UOVA, tipologia=Tipologia.SECONDO, stagione=Stagione.MEZZA),
    Piatto(id=41, nome="Frittata al forno con verdure", tempo=25, adatto_al_lavoro=True, proteina=Proteina.UOVA, tipologia=Tipologia.SECONDO),
    Piatto(id=47, nome="Uova alla coque con crostini", tempo=8, adatto_al_lavoro=False, proteina=Proteina.UOVA, tipologia=Tipologia.SECONDO),
]

def filtro_db(richiesta)-> List[Piatto]:
    return [
        p for p in db 
        if p.tempo <= richiesta.tempo_massimo and (
            richiesta.stagioni is None or 
            p.stagione in richiesta.stagioni or 
            p.stagione == Stagione.GENERICO
        )
    ]

def genera_pool_proteine_garantito() -> List[Proteina]:
    totale_target: int = 14
    # 1. Identifichiamo tutte le proteine che hanno almeno un pasto richiesto
    proteine_richieste = [p for p, qta in frequenza_macro.items() if qta > 0]
    
    # 2. Garanzia: Inseriamo una unità per ogni proteina nel pool finale
    # Questo assicura che nessuna proteina vada a zero
    pool_finale = list(proteine_richieste)
    
    # 3. Creiamo un pool di "avanzi" (tutte le istanze rimanenti oltre la prima già presa)
    rimanenti_pool = []
    for p, qta in frequenza_macro.items():
        # Sottraiamo 1 perché l'abbiamo già messa in pool_finale
        istanze_extra = qta - 1
        if istanze_extra > 0:
            rimanenti_pool.extend([p] * istanze_extra)
    
    # 4. Calcoliamo quanti pasti mancano per arrivare a 14
    posti_da_riempire = totale_target - len(pool_finale)
    
    if posti_da_riempire > 0:
        # Peschiamo casualmente dal pool degli avanzi senza ripetere lo stesso oggetto
        # (random.sample garantisce che non superiamo il limite massimo di ogni proteina)
        extra_estratti = random.sample(rimanenti_pool, k=min(posti_da_riempire, len(rimanenti_pool)))
        pool_finale.extend(extra_estratti)
    
    # 5. Shuffle finale per alternare le fonti durante la settimana
    random.shuffle(pool_finale)
    
    return pool_finale

def seleziona_piatto_da_pool(
    proteina_target: Proteina, 
    vincolo_lavoro: bool, 
    db_filtrato: List[Piatto],
    piatti_gia_usati: List[int] # Nuova lista per evitare duplicati eccessivi
) -> Optional[Piatto]:
    # 1. Cerchiamo i piatti che corrispondono alla proteina del pool e NON sono stati ancora usati
    candidati = [p for p in db_filtrato if p.proteina == proteina_target and p.id not in piatti_gia_usati]
    
    # 2. Se non ci sono piatti nuovi per quella proteina, cerchiamo tra quelli usati 
    # (ma solo se non abbiamo proprio altra scelta per quella specifica proteina)
    if not candidati:
        candidati = [p for p in db_filtrato if p.proteina == proteina_target]

    if vincolo_lavoro:
        candidati_lavoro = [p for p in candidati if p.adatto_al_lavoro]
        if candidati_lavoro:
            candidati = candidati_lavoro

    # 3. Se dopo tutti i filtri non abbiamo piatti per questa proteina, restituiamo None
    if not candidati:
        return None
        
    return random.choice(candidati)

def genera_menu_ordinato(richiesta: Richiesta) -> Risposta:
    # 1. Prepariamo i dati base
    db_filtrato = filtro_db(richiesta)
    pasti_bloccati = richiesta.pasti_bloccati or []
    
    # 2. Mappa per capire subito se un pasto (es. lunedi_pranzo) è bloccato
    mappa_bloccati = {f"{pb.giorno}_{pb.momento}": pb.piatto for pb in pasti_bloccati}
    
    # 3. Aggiorniamo le frequenze: sottraiamo le proteine già scelte manualmente
    frequenza_residua = frequenza_macro.copy()
    for pb in pasti_bloccati:
        if pb.piatto.proteina in frequenza_residua:
            frequenza_residua[pb.piatto.proteina] -= 1

    # 4. Generiamo il pool solo per i posti rimasti (14 totali meno i bloccati)
    pool_proteine = genera_pool_proteine_garantito(frequenza_residua, 14 - len(pasti_bloccati))
    it_pool = iter(pool_proteine)
    
    risultati_giornalieri = {}
    ordine_giorni = ["lunedi", "martedi", "mercoledi", "giovedi", "venerdi", "sabato", "domenica"]
    piatti_usati_ids = []
    conteggio_proteine = {p: 0 for p in Proteina}
    piatto_vuoto = Piatto(id=0, nome="Nessun piatto trovato", tempo=0, adatto_al_lavoro=False)

    for nome_giorno in ordine_giorni:
        enum_giorno = Giorni_settimana[nome_giorno.upper()]
        is_lavorativo = enum_giorno in richiesta.giorni_lavorativi
        pasti_del_giorno = {"pranzo": [], "cena": []}

        for momento in ["pranzo", "cena"]:
            chiave = f"{nome_giorno}_{momento}"
            
            # --- CASO A: IL PASTO È STATO SCELTO DALL'UTENTE ---
            if chiave in mappa_bloccati:
                piatto = mappa_bloccati[chiave]
                pasti_del_giorno[momento] = [piatto]
                piatti_usati_ids.append(piatto.id)
                if piatto.proteina:
                    conteggio_proteine[piatto.proteina] += 1
            
            # --- CASO B: GENERAZIONE AUTOMATICA ---
            else:
                prot_target = next(it_pool, None)
                
                # Verifichiamo se possiamo ancora usare questa proteina
                if prot_target and conteggio_proteine[prot_target] < frequenza_macro.get(prot_target, 0):
                    piatto = seleziona_piatto_da_pool(
                        prot_target, 
                        (momento == "pranzo" and is_lavorativo), 
                        db_filtrato, 
                        piatti_usati_ids
                    )
                    
                    if piatto:
                        pasti_del_giorno[momento] = [piatto]
                        piatti_usati_ids.append(piatto.id)
                        conteggio_proteine[prot_target] += 1
                    else:
                        pasti_del_giorno[momento] = [piatto_vuoto]
                else:
                    pasti_del_giorno[momento] = [piatto_vuoto]

        risultati_giornalieri[nome_giorno] = Pasti(
            pranzo=pasti_del_giorno["pranzo"],
            cena=pasti_del_giorno["cena"]
        )

    # 5. Costruzione risposta finale
    tabella = Pasti_settimana(**risultati_giornalieri)
    dt_inizio = richiesta.data_inizio_settimana or date.today()
    giorno_sett_inizio = list(Giorni_settimana)[dt_inizio.weekday()]

    return Risposta(
        giorno_inizio_settimana=giorno_sett_inizio,
        data_inizio_settimana=dt_inizio,
        tabella=tabella
    )
'''
def genera_menu_ordinato(richiesta: Richiesta) -> Risposta:
    db_filtrato = filtro_db(richiesta)
    pool_proteine = genera_pool_proteine_garantito()
    
    risultati_giornalieri = {}
    ordine_giorni = ["lunedi", "martedi", "mercoledi", "giovedi", "venerdi", "sabato", "domenica"]
    it_pool = iter(pool_proteine)
    
    # Teniamo traccia degli ID piatti usati e del conteggio proteine
    piatti_usati_ids = []
    conteggio_proteine = {p: 0 for p in Proteina}
    
    # Messaggio di errore se il DB filtrato è troppo povero
    piatto_vuoto = Piatto(id=0, nome="Nessun piatto trovato", descrizione="Cambia filtri", tempo=0, adatto_al_lavoro=False)

    for nome_giorno in ordine_giorni:
        enum_giorno = Giorni_settimana[nome_giorno.upper()]
        is_lavorativo = enum_giorno in richiesta.giorni_lavorativi

        pasti_del_giorno = {"pranzo": [], "cena": []}

        for momento in ["pranzo", "cena"]:
            prot_target = next(it_pool, None)
            
            # Verifichiamo se abbiamo già raggiunto il limite per questa proteina
            if prot_target and conteggio_proteine[prot_target] < frequenza_macro.get(prot_target, 0):
                piatto = seleziona_piatto_da_pool(prot_target, (momento == "pranzo" and is_lavorativo), db_filtrato, piatti_usati_ids)
                
                if piatto:
                    pasti_del_giorno[momento] = [piatto]
                    piatti_usati_ids.append(piatto.id)
                    conteggio_proteine[prot_target] += 1
                else:
                    pasti_del_giorno[momento] = [piatto_vuoto]
            else:
                pasti_del_giorno[momento] = [piatto_vuoto]

        risultati_giornalieri[nome_giorno] = Pasti(
            pranzo=pasti_del_giorno["pranzo"],
            cena=pasti_del_giorno["cena"]
        )

    # --- COSTRUZIONE RISPOSTA FINALE ---
    tabella = Pasti_settimana(**risultati_giornalieri)
    
    dt_inizio = richiesta.data_inizio_settimana or date.today()
    giorno_sett_inizio = list(Giorni_settimana)[dt_inizio.weekday()]

    return Risposta(
        giorno_inizio_settimana=giorno_sett_inizio,
        data_inizio_settimana=dt_inizio,
        tabella=tabella
    )
    '''