import pandas as pd
from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Carregar tabela CSV
file_path = '../1_bases_tratadas/basestratadas.csv'  
data = pd.read_csv(file_path)

# Identificar as colunas da tabela CSV
data_split = data['empresas;valor;change;change2'].str.split(';', expand=True)
data_split.columns = ['empresas', 'valor', 'change', 'change2']

# Colocar os tipos de dados
data_split['valor'] = pd.to_numeric(data_split['valor'], errors='coerce')
data_split['change'] = pd.to_numeric(data_split['change'], errors='coerce')
data_split['change2'] = pd.to_numeric(data_split['change2'], errors='coerce')

# Configurar a tabela database .db (=class) pelo SQLAlchemy
Base = declarative_base()

class Empresa(Base):
    __tablename__ = 'yahootable'
    id = Column(Integer, primary_key=True, autoincrement=True)
    empresas = Column(String, nullable=False)
    valor = Column(Float, nullable=False)
    change = Column(Float, nullable=False)
    change2 = Column(Float, nullable=False)

# Criar o banco de dados SQLite
engine = create_engine('sqlite:///yahootable.db')  
Base.metadata.create_all(engine)

# Configurar sessão
Session = sessionmaker(bind=engine)
session = Session()

# Inserir os dados
empresas_list = [
    Empresa(empresas=row['empresas'], valor=row['valor'], change=row['change'], change2=row['change2'])
    for _, row in data_split.iterrows()
]
session.add_all(empresas_list)
session.commit()

print("Arquivo .db criado com sucesso!")
