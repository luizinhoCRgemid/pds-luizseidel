from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///petshop.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Dono(db.Model):
    __tablename__ = "donos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    pets = db.relationship("Pet", backref="dono", lazy=True)


class Pet(db.Model):
    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    dono_id = db.Column(db.Integer, db.ForeignKey("donos.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "especie": self.especie,
            "idade": self.idade,
            "dono_id": self.dono_id,
            "dono_nome": self.dono.nome
        }
 # O objeto que representa o banco inteiro
db = SQLAlchemy(app)


# ---------------------------------------------------------------
# ROTAS DE DONOS - CODIGO DE REFERENCIA
# Estas rotas ja estao prontas. Use elas como modelo para escrever
# as rotas de pets mais abaixo.
# ---------------------------------------------------------------

@app.route("/donos/<int:dono_id>/pets", methods=["GET"])
def listar_pets_do_dono(dono_id):
    dono = db.session.get(Dono, dono_id)

    if dono is None:
        return jsonify({"erro": "Dono nao encontrado"}), 404

    return jsonify([pet.to_dict() for pet in dono.pets])
@app.route("/donos", methods=["GET"])
def listar_donos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, telefone FROM donos")
    linhas = cursor.fetchall()
    conexao.close()

    donos = []
    for linha in linhas:
        donos.append({
            "id": linha[0],
            "nome": linha[1],
            "telefone": linha[2]
        })

    return jsonify(donos)


@app.route("/donos/<int:dono_id>", methods=["GET"])
def buscar_dono(dono_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, nome, telefone FROM donos WHERE id = ?",
        (dono_id,)
    )
    linha = cursor.fetchone()
    conexao.close()

    if linha is None:
        return jsonify({"erro": "Dono nao encontrado"}), 404

    dono = {
        "id": linha[0],
        "nome": linha[1],
        "telefone": linha[2]
    }

    return jsonify(dono)


@app.route("/donos", methods=["POST"])
def criar_dono():
    dados = request.json

    if not dados or "nome" not in dados or "telefone" not in dados:
        return jsonify({"erro": "Informe nome e telefone"}), 400

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO donos (nome, telefone) VALUES (?, ?)",
        (dados["nome"], dados["telefone"])
    )
    conexao.commit()
    novo_id = cursor.lastrowid
    conexao.close()

    dono = {
        "id": novo_id,
        "nome": dados["nome"],
        "telefone": dados["telefone"]
    }

    return jsonify(dono), 201


@app.route("/donos/<int:dono_id>", methods=["PUT"])
def atualizar_dono(dono_id):
    dados = request.json

    if not dados or "nome" not in dados or "telefone" not in dados:
        return jsonify({"erro": "Informe nome e telefone"}), 400

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE donos SET nome = ?, telefone = ? WHERE id = ?",
        (dados["nome"], dados["telefone"], dono_id)
    )
    conexao.commit()
    alterados = cursor.rowcount
    conexao.close()

    if alterados == 0:
        return jsonify({"erro": "Dono nao encontrado"}), 404

    dono = {
        "id": dono_id,
        "nome": dados["nome"],
        "telefone": dados["telefone"]
    }

    return jsonify(dono)


@app.route("/donos/<int:dono_id>", methods=["DELETE"])
def remover_dono(dono_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM donos WHERE id = ?", (dono_id,))
    conexao.commit()
    removidos = cursor.rowcount
    conexao.close()

    if removidos == 0:
        return jsonify({"erro": "Dono nao encontrado"}), 404

    return jsonify({"mensagem": "Dono removido com sucesso"})


@app.route("/pets", methods=["GET"])
def listar_pets():
    dono_id = request.args.get("dono_id")

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        SELECT pets.id, pets.nome, pets.especie, pets.idade,
               pets.dono_id, donos.nome
        FROM pets
        JOIN donos ON pets.dono_id = donos.id
    """

    if dono_id:
        sql += " WHERE pets.dono_id = ?"
        cursor.execute(sql, (dono_id,))
    else:
        cursor.execute(sql)

    linhas = cursor.fetchall()
    conexao.close()

    pets = []
    for linha in linhas:
        pets.append({
            "id": linha[0],
            "nome": linha[1],
            "especie": linha[2],
            "idade": linha[3],
            "dono_id": linha[4],
            "dono_nome": linha[5]
        })

    return jsonify(pets)


@app.route("/pets/<int:pet_id>", methods=["GET"])
def buscar_pet(pet_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, nome, especie, idade, dono_id FROM pets WHERE id = ?",
        (pet_id,)
    )
    linha = cursor.fetchone()
    conexao.close()

    if linha is None:
        return jsonify({"erro": "Pet nao encontrado"}), 404

    pet = {
        "id": linha[0],
        "nome": linha[1],
        "especie": linha[2],
        "idade": linha[3],
        "dono_id": linha[4]
    }

    return jsonify(pet)


@app.route("/pets", methods=["POST"])
def criar_pet():
    dados = request.json

    campos_obrigatorios = ["nome", "especie", "idade", "dono_id"]
    if not dados or not all(campo in dados for campo in campos_obrigatorios):
        return jsonify({"erro": "Informe nome, especie, idade e dono_id"}), 400

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO pets (nome, especie, idade, dono_id) VALUES (?, ?, ?, ?)",
        (dados["nome"], dados["especie"], dados["idade"], dados["dono_id"])
    )
    conexao.commit()
    novo_id = cursor.lastrowid
    conexao.close()

    pet = {
        "id": novo_id,
        "nome": dados["nome"],
        "especie": dados["especie"],
        "idade": dados["idade"],
        "dono_id": dados["dono_id"]
    }

    return jsonify(pet), 201


@app.route("/pets/<int:pet_id>", methods=["PUT"])
def atualizar_pet(pet_id):
    dados = request.json

    campos_obrigatorios = ["nome", "especie", "idade", "dono_id"]
    if not dados or not all(campo in dados for campo in campos_obrigatorios):
        return jsonify({"erro": "Informe nome, especie, idade e dono_id"}), 400

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE pets SET nome = ?, especie = ?, idade = ?, dono_id = ? WHERE id = ?",
        (dados["nome"], dados["especie"], dados["idade"], dados["dono_id"], pet_id)
    )
    conexao.commit()
    alterados = cursor.rowcount
    conexao.close()

    if alterados == 0:
        return jsonify({"erro": "Pet nao encontrado"}), 404

    pet = {
        "id": pet_id,
        "nome": dados["nome"],
        "especie": dados["especie"],
        "idade": dados["idade"],
        "dono_id": dados["dono_id"]
    }

    return jsonify(pet)


@app.route("/pets/<int:pet_id>", methods=["DELETE"])
def remover_pet(pet_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM pets WHERE id = ?", (pet_id,))
    conexao.commit()
    removidos = cursor.rowcount
    conexao.close()

    if removidos == 0:
        return jsonify({"erro": "Pet nao encontrado"}), 404

    return jsonify({"mensagem": "Pet removido com sucesso"})


if __name__ == "__main__":
    app.run(debug=True)
[
{
"id": 1,
"nome": "Rex",
"especie": "cachorro",
"idade": 4,
"dono_id": 1,
"dono_nome": "Ana Paula Ribeiro"
}
]

{
"nome": "Bidu",
"especie": "cachorro",
"idade": 2,
"dono_id": 1
}
