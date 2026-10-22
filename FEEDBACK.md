# Feedback das Aulas 01 e 02

A Aula 01 está feita, mas a Aula 02 ainda não. O app continua usando `sqlite3` nas rotas, e a configuração do SQLAlchemy ficou com espaços no nome da chave e na URI. Corrige para `SQLALCHEMY_DATABASE_URI` e `sqlite:///petshop.db`, cria os modelos e passa as consultas para `db.session`. Inclui `Flask-SQLAlchemy` no requirements e mantém o contrato das rotas.
