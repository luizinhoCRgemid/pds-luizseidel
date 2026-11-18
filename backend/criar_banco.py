import sqlite3

BANCO = "petshop.db"

conexao = sqlite3.connect(BANCO)
cursor = conexao.cursor()

# Apaga as tabelas antigas para o script poder ser rodado de novo
cursor.execute("DROP TABLE IF EXISTS pets")
cursor.execute("DROP TABLE IF EXISTS donos")

cursor.execute("""
CREATE TABLE donos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE pets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    especie TEXT NOT NULL,
    idade INTEGER NOT NULL,
    dono_id INTEGER NOT NULL,
    FOREIGN KEY (dono_id) REFERENCES donos (id)
)
""")

donos = [
    ("Ana Paula Ribeiro", "45999110001"),
    ("Bruno Cardoso", "45999110002"),
    ("Carla Meneghel", "45999110003")
]

for dono in donos:
    cursor.execute("INSERT INTO donos (nome, telefone) VALUES (?, ?)", dono)

pets = [
    ("Rex", "cachorro", 4, 1),
    ("Mimi", "gato", 2, 1),
    ("Thor", "cachorro", 7, 2),
    ("Nina", "gato", 1, 3),
    ("Pingo", "passaro", 3, 3)
]

for pet in pets:
    cursor.execute(
        "INSERT INTO pets (nome, especie, idade, dono_id) VALUES (?, ?, ?, ?)",
        pet
    )

conexao.commit()
conexao.close()

print("Banco criado com sucesso.")
print(f"Foram inseridos {len(donos)} donos e {len(pets)} pets.")
from app import app, db, Dono, Pet

with app.app_context():
    db.drop_all()
    db.create_all()

    print("Banco criado com sucesso!")
    donos = [
    Dono(nome="Ana Paula Ribeiro", telefone="45999110001"),
    Dono(nome="Bruno Cardoso", telefone="45999110002"),
    Dono(nome="Carla Meneghel", telefone="45999110003")
]

db.session.add_all(donos)
db.session.commit()
pets = [
    Pet(nome="Rex", especie="cachorro", idade=4, dono_id=1),
    Pet(nome="Mimi", especie="gato", idade=2, dono_id=1),
    Pet(nome="Thor", especie="cachorro", idade=7, dono_id=2),
    Pet(nome="Nina", especie="gato", idade=1, dono_id=3),
    Pet(nome="Pingo", especie="passaro", idade=3, dono_id=3)
]

db.session.add_all(pets)
db.session.commit()

pets = [
    Pet(nome="Rex", especie="cachorro", idade=4, dono_id=1),
    Pet(nome="Mimi", especie="gato", idade=2, dono_id=1),
    Pet(nome="Thor", especie="cachorro", idade=7, dono_id=2),
    Pet(nome="Nina", especie="gato", idade=1, dono_id=3),
    Pet(nome="Pingo", especie="passaro", idade=3, dono_id=3)
]

db.session.add_all(pets)
db.session.commit()