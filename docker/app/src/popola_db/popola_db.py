import sys
import os
import time
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

# 1. Configurazione del percorso
# All'interno del container, se WORKDIR è /app, lo script vede già la cartella 'src'
sys.path.append(os.getcwd())

try:
    # Importiamo le classi e le enumerazioni dai file del progetto
    from src.database import Base, PiattoDB, MacroDB
    from src.enums import Proteina, Stagione, Tipologia
except ImportError as e:
    print(f"Errore: Non riesco a trovare i moduli nella cartella 'src'. Dettaglio: {e}")
    sys.exit(1)

# --- CONFIGURAZIONE PER ESECUZIONE DENTRO DOCKER ---
# Usiamo 'db' come host perché è il nome del servizio definito nel docker-compose
DB_USER = "menu"
DB_PASS = "menu"
DB_HOST = "db"
DB_NAME = "menu_progetto"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}"

# Configurazione Engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def popola():
    print(f"Inizializzazione database su host: {DB_HOST}...")

    # Tentativi di connessione (il DB potrebbe impiegare tempo per avviarsi)
    db_connesso = False
    for i in range(10):
        try:
            with engine.connect() as connection:
                print("Connessione stabilita.")
                db_connesso = True
                break
        except Exception:
            print(f"Tentativo {i+1}: DB non pronto, attesa...")
            time.sleep(5)

    if not db_connesso:
        sys.exit(1)

    # 1. ASSICURA CHE LE TABELLE ESISTANO (senza cancellarle)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # --- 2. AGGIORNAMENTO MACRO ---
        print("Controllo frequenze macro...")
        macro_predefinite = [
            {"proteina": Proteina.LEGUMI.value, "frequenza": 3},
            {"proteina": Proteina.LATTICINI.value, "frequenza": 4},
            {"proteina": Proteina.CARNE_BIANCA.value, "frequenza": 4},
            {"proteina": Proteina.CARNE_ROSSA.value, "frequenza": 1},
            {"proteina": Proteina.PESCE.value, "frequenza": 3},
            {"proteina": Proteina.UOVA.value, "frequenza": 3},
        ]

        for m_data in macro_predefinite:
            esistente = db.execute(select(MacroDB).filter_by(proteina=m_data["proteina"])).scalar_one_or_none()
            if not esistente:
                db.add(MacroDB(**m_data))

        # --- 3. IMPORTA PIATTI ---
        print("Controllo ricettario...")
        piatti_base = [
            # LATTICINI
            PiattoDB(nome="Pasta al pomodoro e mozzarella", tempo=30, adatto_al_lavoro=False, proteina=Proteina.LATTICINI.value, tipologia=Tipologia.PRIMO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(nome="Tomino alla piastra", tempo=5, adatto_al_lavoro=True, proteina=Proteina.LATTICINI.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(nome="Insalata greca", tempo=10, adatto_al_lavoro=True, proteina=Proteina.LATTICINI.value, tipologia=Tipologia.UNICO.value, stagione=Stagione.ESTATE.value),
            PiattoDB(nome="Gnocchi al gorgonzola", tempo=15, adatto_al_lavoro=False, proteina=Proteina.LATTICINI.value, tipologia=Tipologia.PRIMO.value, stagione=Stagione.INVERNO.value),
            PiattoDB(nome="Pasta fredda tricolore", tempo=20, adatto_al_lavoro=True, proteina=Proteina.LATTICINI.value, tipologia=Tipologia.PRIMO.value, stagione=Stagione.ESTATE.value),
            PiattoDB(nome="Ricotta fresca e miele", tempo=5, adatto_al_lavoro=True, proteina=Proteina.LATTICINI.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.ESTATE.value),

            # LEGUMI
            PiattoDB(nome="Minestrone di verdure", tempo=40, adatto_al_lavoro=False, proteina=Proteina.LEGUMI.value, tipologia=Tipologia.PRIMO.value, stagione=Stagione.INVERNO.value),
            PiattoDB(nome="Insalata di ceci e tonno", tempo=10, adatto_al_lavoro=True, proteina=Proteina.LEGUMI.value, tipologia=Tipologia.UNICO.value, stagione=Stagione.ESTATE.value),
            PiattoDB(nome="Lenticchie in umido", tempo=45, adatto_al_lavoro=True, proteina=Proteina.LEGUMI.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.INVERNO.value),
            PiattoDB(nome="Polpette di soia", tempo=20, adatto_al_lavoro=True, proteina=Proteina.LEGUMI.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(nome="Quinoa con verdure", tempo=25, adatto_al_lavoro=True, proteina=Proteina.LEGUMI.value, tipologia=Tipologia.UNICO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(nome="Fagioli all'uccelletto", tempo=30, adatto_al_lavoro=True, proteina=Proteina.LEGUMI.value, tipologia=Tipologia.CONTORNO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(nome="Hummus con cruditè", tempo=15, adatto_al_lavoro=True, proteina=Proteina.LEGUMI.value, tipologia=Tipologia.UNICO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(nome="Zuppa di farro e lenticchie", tempo=40, adatto_al_lavoro=True, proteina=Proteina.LEGUMI.value, tipologia=Tipologia.UNICO.value, stagione=Stagione.INVERNO.value),
            PiattoDB(nome="Zuppa di piselli freschi", tempo=30, adatto_al_lavoro=False, proteina=Proteina.LEGUMI.value, tipologia=Tipologia.PRIMO.value, stagione=Stagione.MEZZA.value),

            # CARNE BIANCA
            PiattoDB(nome="Hamburger di pollo", tempo=10, adatto_al_lavoro=True, proteina=Proteina.CARNE_BIANCA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(nome="Spiedini di tacchino", tempo=15, adatto_al_lavoro=True, proteina=Proteina.CARNE_BIANCA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(nome="Scaloppine al limone", tempo=15, adatto_al_lavoro=True, proteina=Proteina.CARNE_BIANCA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(nome="Insalata di pollo e mele", tempo=15, adatto_al_lavoro=True, proteina=Proteina.CARNE_BIANCA.value, tipologia=Tipologia.UNICO.value, stagione=Stagione.ESTATE.value),
            PiattoDB(nome="Pollo al curry", tempo=25, adatto_al_lavoro=True, proteina=Proteina.CARNE_BIANCA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.INVERNO.value),
            PiattoDB(nome="Tacchino alle erbe", tempo=15, adatto_al_lavoro=True, proteina=Proteina.CARNE_BIANCA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.MEZZA.value),
            PiattoDB(nome="Bocconcini di pollo ai funghi", tempo=20, adatto_al_lavoro=True, proteina=Proteina.CARNE_BIANCA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.INVERNO.value),

            # CARNE ROSSA
            PiattoDB(nome="Spezzatino di manzo", tempo=90, adatto_al_lavoro=False, proteina=Proteina.CARNE_ROSSA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.INVERNO.value),
            PiattoDB(nome="Straccetti di vitello", tempo=10, adatto_al_lavoro=True, proteina=Proteina.CARNE_ROSSA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(nome="Bistecca ai ferri", tempo=8, adatto_al_lavoro=False, proteina=Proteina.CARNE_ROSSA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(nome="Polpette al sugo", tempo=35, adatto_al_lavoro=False, proteina=Proteina.CARNE_ROSSA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.INVERNO.value),
            PiattoDB(nome="Carpaccio di bresaola", tempo=5, adatto_al_lavoro=True, proteina=Proteina.CARNE_ROSSA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.ESTATE.value),
            PiattoDB(nome="Tagliata di manzo e rucola", tempo=12, adatto_al_lavoro=False, proteina=Proteina.CARNE_ROSSA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.MEZZA.value),

            # PESCE
            PiattoDB(nome="Salmone al vapore", tempo=15, adatto_al_lavoro=True, proteina=Proteina.PESCE.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(nome="Baccalà alla livornese", tempo=40, adatto_al_lavoro=False, proteina=Proteina.PESCE.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(nome="Branzino al sale", tempo=35, adatto_al_lavoro=False, proteina=Proteina.PESCE.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(nome="Cous cous di pesce", tempo=30, adatto_al_lavoro=True, proteina=Proteina.PESCE.value, tipologia=Tipologia.UNICO.value, stagione=Stagione.ESTATE.value),
            PiattoDB(nome="Sogliola alla mugnaia", tempo=10, adatto_al_lavoro=True, proteina=Proteina.PESCE.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.MEZZA.value),
            PiattoDB(nome="Zuppa di pesce", tempo=50, adatto_al_lavoro=False, proteina=Proteina.PESCE.value, tipologia=Tipologia.UNICO.value, stagione=Stagione.INVERNO.value),
            PiattoDB(nome="Filetto di orata al forno", tempo=20, adatto_al_lavoro=False, proteina=Proteina.PESCE.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),

            # UOVA
            PiattoDB(nome="Frittata alle erbe", tempo=15, adatto_al_lavoro=True, proteina=Proteina.UOVA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(nome="Pasta alla carbonara", tempo=20, adatto_al_lavoro=False, proteina=Proteina.UOVA.value, tipologia=Tipologia.PRIMO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(nome="Uova in purgatorio", tempo=15, adatto_al_lavoro=False, proteina=Proteina.UOVA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(nome="Omelette al formaggio", tempo=10, adatto_al_lavoro=False, proteina=Proteina.UOVA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(nome="Uova sode e asparagi", tempo=15, adatto_al_lavoro=True, proteina=Proteina.UOVA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.MEZZA.value),
            PiattoDB(nome="Frittata al forno con verdure", tempo=25, adatto_al_lavoro=True, proteina=Proteina.UOVA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(nome="Uova alla coque con crostini", tempo=8, adatto_al_lavoro=False, proteina=Proteina.UOVA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
        ]

        nuovi_inseriti = 0
        for piatto in piatti_base:
            # Controlla se esiste già un piatto con lo stesso nome
            esistente = db.execute(select(PiattoDB).filter_by(nome=piatto.nome)).scalar_one_or_none()
            if not esistente:
                db.add(piatto)
                nuovi_inseriti += 1

        db.commit()
        print(f"Operazione completata. Nuovi piatti aggiunti: {nuovi_inseriti}.")

    except Exception as e:
        print(f"Errore durante il popolamento: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    popola()
