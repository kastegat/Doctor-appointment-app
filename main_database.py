from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Boolean, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


engine = create_engine("sqlite:///management_system.db")
Base = declarative_base()

# Duomenų bazės lentelių sukūrimas, ryšiai.
class Pacientai(Base):
    __tablename__ = 'pacientai'
    vardas = Column(String, nullable=False)
    pavarde = Column(String, nullable=False)
    slaptazodis = Column(String, nullable=False)
    asmens_kodas = Column(Integer, nullable=False)
    tel_nr = Column(Integer, nullable=False)
    el_pastas = Column(String, primary_key=True, unique=True)
    lytis = Column(String, nullable=False)
    gimimo_data = Column(String, nullable=False)
    apsilankymas_rel = relationship("Apsilankymai", back_populates='pacient_rel')

    def __init__(self, vardas, pavarde, slaptazodis, asmens_kodas, tel_nr, el_pastas, lytis, gimimo_data):
        self.vardas = vardas
        self.pavarde = pavarde
        self.slaptazodis = slaptazodis
        self.asmens_kodas = asmens_kodas
        self.tel_nr = tel_nr
        self.el_pastas = el_pastas
        self.lytis = lytis
        self.gimimo_data = gimimo_data

    def __repr__(self):
        return f'VARDAS:{self.vardas} ' \
               f'PAVARDĖ:{self.pavarde} ' \
               f'ASMENS KODAS:{self.asmens_kodas} ' \
               f'TEL.NUMERIS:{self.tel_nr}'


class Daktarai(Base):
    __tablename__ = 'daktarai'
    id = Column(Integer, primary_key=True)
    vardas = Column(String, nullable=False)
    pavarde = Column(String, nullable=False)
    specializacija = Column(String, nullable=False)
    el_pastas = Column(String, unique=True)
    apsilankymas2_rel = relationship("Apsilankymai", back_populates='daktar_rel')

    def __init__(self, vardas, pavarde, specializacija, el_pastas):
        self.vardas = vardas
        self.pavarde = pavarde
        self.specializacija = specializacija
        self.el_pastas = el_pastas


class Apsilankymai(Base):
    __tablename__ = 'apsilankymai'
    id = Column(Integer, primary_key=True)
    data = Column(String, nullable=False)
    laikas = Column(String, nullable=False)
    priezastis = Column(Text, nullable=False)
    daktaras_id = Column(String, ForeignKey('daktarai.el_pastas'))
    pacientas_id = Column(Integer, ForeignKey('pacientai.el_pastas'))
    daktar_rel = relationship("Daktarai", back_populates='apsilankymas2_rel')
    pacient_rel = relationship("Pacientai", back_populates='apsilankymas_rel')

    def __init__(self, data, laikas, priezastis):
        self.data = data
        self.laikas = laikas
        self.priezastis = priezastis

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()




