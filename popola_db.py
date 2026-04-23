from src.database import SessionLocal, PiattoDB, MacroDB, init_db
from src.enums import Proteina, Stagione, Tipologia

def popola():
    # 1. Crea il file database e le tabelle se non esistono
    print("Inizializzazione database...")
    init_db()
    
    db = SessionLocal()
    
    try:
        # Pulizia opzionale: evita duplicati se lanci lo script più volte
        db.query(PiattoDB).delete()
        db.query(MacroDB).delete()

        # --- 2. IMPORTA MACRO ---
        print("Importazione frequenze macro...")
        frequenze = [
            MacroDB(proteina=Proteina.LEGUMI.value, frequenza=3),
            MacroDB(proteina=Proteina.LATTICINI.value, frequenza=4),
            MacroDB(proteina=Proteina.CARNE_BIANCA.value, frequenza=4),
            MacroDB(proteina=Proteina.CARNE_ROSSA.value, frequenza=1),
            MacroDB(proteina=Proteina.PESCE.value, frequenza=3),
            MacroDB(proteina=Proteina.UOVA.value, frequenza=3),
        ]
        db.add_all(frequenze)

        # --- 3. IMPORTA PIATTI ---
        print("Importazione ricettario...")
        lista_piatti = [
            # LATTICINI
            PiattoDB(id=1, nome="Pasta al pomodoro e mozzarella", tempo=30, adatto_al_lavoro=False, proteina=Proteina.LATTICINI.value, tipologia=Tipologia.PRIMO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(id=2, nome="Tomino alla piastra", tempo=5, adatto_al_lavoro=True, proteina=Proteina.LATTICINI.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(id=12, nome="Insalata greca", tempo=10, adatto_al_lavoro=True, proteina=Proteina.LATTICINI.value, tipologia=Tipologia.UNICO.value, stagione=Stagione.ESTATE.value),
            PiattoDB(id=20, nome="Gnocchi al gorgonzola", tempo=15, adatto_al_lavoro=False, proteina=Proteina.LATTICINI.value, tipologia=Tipologia.PRIMO.value, stagione=Stagione.INVERNO.value),
            PiattoDB(id=22, nome="Pasta fredda tricolore", tempo=20, adatto_al_lavoro=True, proteina=Proteina.LATTICINI.value, tipologia=Tipologia.PRIMO.value, stagione=Stagione.ESTATE.value),
            PiattoDB(id=31, nome="Ricotta fresca e miele", tempo=5, adatto_al_lavoro=True, proteina=Proteina.LATTICINI.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.ESTATE.value),

            # LEGUMI
            PiattoDB(id=3, nome="Minestrone di verdure", tempo=40, adatto_al_lavoro=False, proteina=Proteina.LEGUMI.value, tipologia=Tipologia.PRIMO.value, stagione=Stagione.INVERNO.value),
            PiattoDB(id=5, nome="Insalata di ceci e tonno", tempo=10, adatto_al_lavoro=True, proteina=Proteina.LEGUMI.value, tipologia=Tipologia.UNICO.value, stagione=Stagione.ESTATE.value),
            PiattoDB(id=11, nome="Lenticchie in umido", tempo=45, adatto_al_lavoro=True, proteina=Proteina.LEGUMI.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.INVERNO.value),
            PiattoDB(id=16, nome="Polpette di soia", tempo=20, adatto_al_lavoro=True, proteina=Proteina.LEGUMI.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(id=17, nome="Quinoa con verdure", tempo=25, adatto_al_lavoro=True, proteina=Proteina.LEGUMI.value, tipologia=Tipologia.UNICO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(id=23, nome="Fagioli all'uccelletto", tempo=30, adatto_al_lavoro=True, proteina=Proteina.LEGUMI.value, tipologia=Tipologia.CONTORNO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(id=28, nome="Hummus con cruditè", tempo=15, adatto_al_lavoro=True, proteina=Proteina.LEGUMI.value, tipologia=Tipologia.UNICO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(id=30, nome="Zuppa di farro e lenticchie", tempo=40, adatto_al_lavoro=True, proteina=Proteina.LEGUMI.value, tipologia=Tipologia.UNICO.value, stagione=Stagione.INVERNO.value),
            PiattoDB(id=32, nome="Zuppa di piselli freschi", tempo=30, adatto_al_lavoro=False, proteina=Proteina.LEGUMI.value, tipologia=Tipologia.PRIMO.value, stagione=Stagione.MEZZA.value),

            # CARNE BIANCA
            PiattoDB(id=4, nome="Hamburger di pollo", tempo=10, adatto_al_lavoro=True, proteina=Proteina.CARNE_BIANCA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(id=19, nome="Spiedini di tacchino", tempo=15, adatto_al_lavoro=True, proteina=Proteina.CARNE_BIANCA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(id=27, nome="Scaloppine al limone", tempo=15, adatto_al_lavoro=True, proteina=Proteina.CARNE_BIANCA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(id=33, nome="Insalata di pollo e mele", tempo=15, adatto_al_lavoro=True, proteina=Proteina.CARNE_BIANCA.value, tipologia=Tipologia.UNICO.value, stagione=Stagione.ESTATE.value),
            PiattoDB(id=34, nome="Pollo al curry", tempo=25, adatto_al_lavoro=True, proteina=Proteina.CARNE_BIANCA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.INVERNO.value),
            PiattoDB(id=35, nome="Tacchino alle erbe", tempo=15, adatto_al_lavoro=True, proteina=Proteina.CARNE_BIANCA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.MEZZA.value),
            PiattoDB(id=44, nome="Bocconcini di pollo ai funghi", tempo=20, adatto_al_lavoro=True, proteina=Proteina.CARNE_BIANCA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.INVERNO.value),

            # CARNE ROSSA
            PiattoDB(id=10, nome="Spezzatino di manzo", tempo=90, adatto_al_lavoro=False, proteina=Proteina.CARNE_ROSSA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.INVERNO.value),
            PiattoDB(id=13, nome="Straccetti di vitello", tempo=10, adatto_al_lavoro=True, proteina=Proteina.CARNE_ROSSA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(id=24, nome="Bistecca ai ferri", tempo=8, adatto_al_lavoro=False, proteina=Proteina.CARNE_ROSSA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(id=36, nome="Polpette al sugo", tempo=35, adatto_al_lavoro=False, proteina=Proteina.CARNE_ROSSA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.INVERNO.value),
            PiattoDB(id=37, nome="Carpaccio di bresaola", tempo=5, adatto_al_lavoro=True, proteina=Proteina.CARNE_ROSSA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.ESTATE.value),
            PiattoDB(id=45, nome="Tagliata di manzo e rucola", tempo=12, adatto_al_lavoro=False, proteina=Proteina.CARNE_ROSSA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.MEZZA.value),

            # PESCE
            PiattoDB(id=8, nome="Salmone al vapore", tempo=15, adatto_al_lavoro=True, proteina=Proteina.PESCE.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(id=15, nome="Baccalà alla livornese", tempo=40, adatto_al_lavoro=False, proteina=Proteina.PESCE.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(id=21, nome="Branzino al sale", tempo=35, adatto_al_lavoro=False, proteina=Proteina.PESCE.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(id=26, nome="Cous cous di pesce", tempo=30, adatto_al_lavoro=True, proteina=Proteina.PESCE.value, tipologia=Tipologia.UNICO.value, stagione=Stagione.ESTATE.value),
            PiattoDB(id=38, nome="Sogliola alla mugnaia", tempo=10, adatto_al_lavoro=True, proteina=Proteina.PESCE.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.MEZZA.value),
            PiattoDB(id=39, nome="Zuppa di pesce", tempo=50, adatto_al_lavoro=False, proteina=Proteina.PESCE.value, tipologia=Tipologia.UNICO.value, stagione=Stagione.INVERNO.value),
            PiattoDB(id=46, nome="Filetto di orata al forno", tempo=20, adatto_al_lavoro=False, proteina=Proteina.PESCE.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),

            # UOVA
            PiattoDB(id=7, nome="Frittata alle erbe", tempo=15, adatto_al_lavoro=True, proteina=Proteina.UOVA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(id=9, nome="Pasta alla carbonara", tempo=20, adatto_al_lavoro=False, proteina=Proteina.UOVA.value, tipologia=Tipologia.PRIMO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(id=18, nome="Uova in purgatorio", tempo=15, adatto_al_lavoro=False, proteina=Proteina.UOVA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(id=29, nome="Omelette al formaggio", tempo=10, adatto_al_lavoro=False, proteina=Proteina.UOVA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(id=40, nome="Uova sode e asparagi", tempo=15, adatto_al_lavoro=True, proteina=Proteina.UOVA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.MEZZA.value),
            PiattoDB(id=41, nome="Frittata al forno con verdure", tempo=25, adatto_al_lavoro=True, proteina=Proteina.UOVA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
            PiattoDB(id=47, nome="Uova alla coque con crostini", tempo=8, adatto_al_lavoro=False, proteina=Proteina.UOVA.value, tipologia=Tipologia.SECONDO.value, stagione=Stagione.GENERICO.value),
        ]
        
        db.add_all(lista_piatti)
        db.commit()
        print(f"Completato! Caricati {len(lista_piatti)} piatti.")

    except Exception as e:
        print(f"Errore durante il popolamento: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    popola()