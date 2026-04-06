import random
from typing import Dict, List

from src.risposta_menu import Risposta
from src.piatto import Piatto
from src.enums import Giorni_settimana, Proteina, Stagione, Tipologia
from src.richiesta_menu import Richiesta

frequenza_macro = Dict[Proteina, int] = {
    Proteina.LEGUMI: 3,        # Es: Lunedì pranzo, Mercoledì cena, Venerdì pranzo
    Proteina.LATTICINI: 2,     # Es: Martedì cena, Sabato pranzo
    Proteina.CARNE_BIANCA: 3,  # Es: Lunedì cena, Giovedì pranzo, Sabato cena
    Proteina.CARNE_ROSSA: 1,   # Es: Domenica pranzo
    Proteina.PESCE: 3,         # Es: Martedì pranzo, Venerdì cena, Domenica cena
    Proteina.UOVA: 2           # Es: Mercoledì pranzo, Giovedì cena
}

db: List[Piatto] = [
    Piatto(id=1, nome="Pasta al pomodoro e mozzarella", tempo=30, adatto_al_lavoro=False, proteina=Proteina.LATTICINI, tipologia=Tipologia.PRIMO),
    Piatto(id=2, nome="Tomino alla piastra", tempo=5, adatto_al_lavoro=True, proteina=Proteina.LATTICINI, tipologia=Tipologia.SECONDO),
    Piatto(id=3, nome="Minestrone di verdure", tempo=40, adatto_al_lavoro=False, proteina=Proteina.LEGUMI, tipologia=Tipologia.PRIMO, stagione=Stagione.INVERNO),
    Piatto(id=4, nome="Hamburger di pollo", tempo=10, adatto_al_lavoro=True, proteina=Proteina.CARNE_BIANCA, tipologia=Tipologia.SECONDO),
    Piatto(id=5, nome="Insalata di ceci e tonno", tempo=10, adatto_al_lavoro=True, proteina=Proteina.LEGUMI, tipologia=Tipologia.UNICO, stagione=Stagione.ESTATE),
    Piatto(id=6, nome="Risotto ai funghi", tempo=25, adatto_al_lavoro=False, proteina=None, tipologia=Tipologia.PRIMO, stagione=Stagione.INVERNO),
    Piatto(id=7, nome="Frittata alle erbe", tempo=15, adatto_al_lavoro=True, proteina=Proteina.UOVA, tipologia=Tipologia.SECONDO),
    Piatto(id=8, nome="Salmone al vapore", tempo=15, adatto_al_lavoro=True, proteina=Proteina.PESCE, tipologia=Tipologia.SECONDO),
    Piatto(id=9, nome="Pasta alla carbonara", tempo=20, adatto_al_lavoro=False, proteina=Proteina.UOVA, tipologia=Tipologia.PRIMO),
    Piatto(id=10, nome="Spezzatino di manzo", tempo=90, adatto_al_lavoro=False, proteina=Proteina.CARNE_ROSSA, tipologia=Tipologia.SECONDO, stagione=Stagione.INVERNO),
    Piatto(id=11, nome="Lenticchie in umido", tempo=45, adatto_al_lavoro=True, proteina=Proteina.LEGUMI, tipologia=Tipologia.SECONDO, stagione=Stagione.INVERNO),
    Piatto(id=12, nome="Insalata greca", tempo=10, adatto_al_lavoro=True, proteina=Proteina.LATTICINI, tipologia=Tipologia.UNICO, stagione=Stagione.ESTATE),
    Piatto(id=13, nome="Straccetti di vitello", tempo=10, adatto_al_lavoro=True, proteina=Proteina.CARNE_ROSSA, tipologia=Tipologia.SECONDO),
    Piatto(id=14, nome="Pasta integrale alle zucchine", tempo=20, adatto_al_lavoro=True, proteina=None, tipologia=Tipologia.PRIMO, stagione=Stagione.MEZZA),
    Piatto(id=15, nome="Baccalà alla livornese", tempo=40, adatto_al_lavoro=False, proteina=Proteina.PESCE, tipologia=Tipologia.SECONDO),
    Piatto(id=16, nome="Polpette di soia", tempo=20, adatto_al_lavoro=True, proteina=Proteina.LEGUMI, tipologia=Tipologia.SECONDO),
    Piatto(id=17, nome="Quinoa con verdure", tempo=25, adatto_al_lavoro=True, proteina=Proteina.LEGUMI, tipologia=Tipologia.UNICO),
    Piatto(id=18, nome="Uova in purgatorio", tempo=15, adatto_al_lavoro=False, proteina=Proteina.UOVA, tipologia=Tipologia.SECONDO),
    Piatto(id=19, nome="Spiedini di tacchino", tempo=15, adatto_al_lavoro=True, proteina=Proteina.CARNE_BIANCA, tipologia=Tipologia.SECONDO),
    Piatto(id=20, nome="Gnocchi al gorgonzola", tempo=15, adatto_al_lavoro=False, proteina=Proteina.LATTICINI, tipologia=Tipologia.PRIMO, stagione=Stagione.INVERNO),
    Piatto(id=21, nome="Branzino al sale", tempo=35, adatto_al_lavoro=False, proteina=Proteina.PESCE, tipologia=Tipologia.SECONDO),
    Piatto(id=22, nome="Pasta fredda tricolore", tempo=20, adatto_al_lavoro=True, proteina=Proteina.LATTICINI, tipologia=Tipologia.PRIMO, stagione=Stagione.ESTATE),
    Piatto(id=23, nome="Fagioli all'uccelletto", tempo=30, adatto_al_lavoro=True, proteina=Proteina.LEGUMI, tipologia=Tipologia.CONTORNO),
    Piatto(id=24, nome="Bistecca ai ferri", tempo=8, adatto_al_lavoro=False, proteina=Proteina.CARNE_ROSSA, tipologia=Tipologia.SECONDO),
    Piatto(id=25, nome="Vellutata di zucca", tempo=35, adatto_al_lavoro=True, proteina=None, tipologia=Tipologia.PRIMO, stagione=Stagione.INVERNO),
    Piatto(id=26, nome="Cous cous di pesce", tempo=30, adatto_al_lavoro=True, proteina=Proteina.PESCE, tipologia=Tipologia.UNICO, stagione=Stagione.ESTATE),
    Piatto(id=27, nome="Scaloppine al limone", tempo=15, adatto_al_lavoro=True, proteina=Proteina.CARNE_BIANCA, tipologia=Tipologia.SECONDO),
    Piatto(id=28, nome="Hummus con cruditè", tempo=15, adatto_al_lavoro=True, proteina=Proteina.LEGUMI, tipologia=Tipologia.UNICO),
    Piatto(id=29, nome="Omelette al formaggio", tempo=10, adatto_al_lavoro=False, proteina=Proteina.UOVA, tipologia=Tipologia.SECONDO),
    Piatto(id=30, nome="Zuppa di farro e lenticchie", tempo=40, adatto_al_lavoro=True, proteina=Proteina.LEGUMI, tipologia=Tipologia.UNICO, stagione=Stagione.INVERNO),
]

def genera_piano_settimanale(richiesta: Richiesta) -> Risposta:
    
    import random
from datetime import date
from typing import List, Dict, Optional

def genera_menu_ordinato(
    richiesta: Richiesta, 
    db: List[Piatto], 
    frequenza_macro: Dict[Proteina, int]
) -> Risposta:
    
    # --- PUNTO 1: Filtrare il DB ---
    # Includiamo sempre Stagione.GENERICO e filtriamo per tempo_massimo
    db_filtrato = [
        p for p in db 
        if p.tempo <= richiesta.tempo_massimo and (
            richiesta.stagioni is None or 
            p.stagione in richiesta.stagioni or 
            p.stagione == Stagione.GENERICO
        )
    ]

    # --- PUNTO 2: Crea pool di proteine (Shuffle) ---
    # Creiamo una lista di 14 elementi basata sulle frequenze desiderate
    ##### DA RAFFINARE IN UN SEGONDO MOMENTO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    pool_proteine = []
    for prot, limite_massimo in frequenza_macro.items():
        pool_proteine.extend([prot] * limite_massimo)
    
    # Assicuriamoci che il pool sia esattamente di 14 (o gestiamo il resto)
    random.shuffle(pool_proteine)

    # --- PUNTO 3: Assegnazione piatti e gestione giorni lavorativi ---
    
    def seleziona_piatto_da_pool(proteina_target: Proteina, vincolo_lavoro: bool) -> Piatto:
        # Cerchiamo i piatti che corrispondono alla proteina del pool
        candidati = [p for p in db_filtrato if p.proteina == proteina_target]
        
        if vincolo_lavoro:
            # Filtro stringente: solo piatti adatti al lavoro
            candidati_lavoro = [p for p in candidati if p.adatto_al_lavoro]
            # Se esistono piatti specifici per il lavoro li usiamo, 
            # altrimenti fallback sui candidati generici di quella proteina
            if candidati_lavoro:
                candidati = candidati_lavoro

        if not candidati:
            # Fallback estremo: se non ci sono piatti per quella proteina nel DB filtrato, 
            # ne cerchiamo uno qualsiasi nel DB filtrato per non rompere l'esecuzione
            return random.choice(db_filtrato) if db_filtrato else Piatto(id=0, nome="N/A", tempo=0, adatto_al_lavoro=False)
            
        return random.choice(candidati)

    # Costruiamo la tabella giorno per giorno
    risultati_giornalieri = {}
    ordine_giorni = ["lunedi", "martedi", "mercoledi", "giovedi", "venerdi", "sabato", "domenica"]
    
    # Usiamo un iteratore sul pool per prelevare le proteine "in maniera ordinata dallo shuffle"
    it_pool = iter(pool_proteine)

    for nome_giorno in ordine_giorni:
        enum_giorno = Giorni_settimana[nome_giorno.upper()]
        is_lavorativo = enum_giorno in richiesta.giorni_lavorativi

        # Estrazione ordinata dal pool rimescolato
        prot_pranzo = next(it_pool, None)
        prot_cena = next(it_pool, None)

        # Creazione oggetto Pasti (usando le tue classi)
        risultati_giornalieri[nome_giorno] = Pasti(
            pranzo=[seleziona_piatto_da_pool(prot_pranzo, is_lavorativo)],
            cena=[seleziona_piatto_da_pool(prot_cena, False)]
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




def crea_menu (richiesta: Richiesta) -> Risposta:
    