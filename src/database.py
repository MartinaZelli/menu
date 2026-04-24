from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Date, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Creazione del file unico (verrà creato automaticamente)
DATABASE_URL = "sqlite:///./menu_progetto.db"
Base = declarative_base()

# --- TABELLA MACRO ---
class MacroDB(Base):
    __tablename__ = "macro"
    id = Column(Integer, primary_key=True, index=True)
    proteina = Column(String, unique=True) # Es: "carne bianca"
    frequenza = Column(Integer)            # Es: 4

# --- TABELLA PIATTO ---
class PiattoDB(Base):
    __tablename__ = "piatti"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    proteina = Column(String)
    stagione = Column(String)
    tempo = Column(Integer)
    adatto_al_lavoro = Column(Boolean)
    tipologia = Column(String)

# --- TABELLA TOTALE (Settimana) ---
class SettimanaDB(Base):
    __tablename__ = "settimane"
    id = Column(Integer, primary_key=True, index=True)
    data_inizio = Column(Date, unique=True)
    # Relazione con i singoli pasti salvati
    pasti = relationship("PastoSalvatoDB", back_populates="settimana")

# --- TABELLA D'APPOGGIO PER I PASTI DEL MENU ---
class PastoSalvatoDB(Base):
    __tablename__ = "pasti_salvati"
    id = Column(Integer, primary_key=True, index=True)
    settimana_id = Column(Integer, ForeignKey("settimane.id"))
    giorno = Column(String)  # lunedi, martedi...
    momento = Column(String) # pranzo, cena
    piatto_id = Column(Integer, ForeignKey("piatti.id"))
    nome_manuale = Column(String, nullable=True) # <--- AGGIUNGI QUESTA RIGA
    
    settimana = relationship("SettimanaDB", back_populates="pasti")
    piatto = relationship("PiattoDB")

# Setup finale
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)