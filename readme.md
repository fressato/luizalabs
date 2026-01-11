# WorkoutAPI

API de gerenciamento de academias e treinos, desenvolvida utilizando **FastAPI**.

## � Tecnologias

- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework web moderno e rápido.
- **[Uvicorn](https://www.uvicorn.org/)**: Servidor ASGI.
- **[SQLAlchemy](https://www.sqlalchemy.org/)**: ORM para manipulação do banco de dados.
- **[Alembic](https://alembic.sqlalchemy.org/)**: Ferramenta de migração de banco de dados.
- **[Pydantic](https://docs.pydantic.dev/)**: Validação de dados.

## 🛠️ Como Executar

Siga os passos abaixo para configurar e rodar o projeto localmente.

### Pré-requisitos

- Python 3.11+
- Pip (Gerenciador de pacotes do Python)

### Instalação

1. Clone o repositório e entre na pasta do projeto:
   ```bash
   git clone https://github.com/seurepositorio/workoutapi.git
   cd luizalabs
   ```

2. Crie um ambiente virtual (opcional, mas recomendado) e instale as dependências:
   ```bash
   python -m venv venv
   # No Windows
   venv\Scripts\activate
   # No Linux/Mac
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

### Banco de Dados e Migrações

O projeto utiliza `Makefile` para facilitar comandos comuns. Para criar as tabelas no banco de dados, execute:

```bash
make run-migrations
```

Isso executará o `alembic upgrade head`.

### Executando a API

Para iniciar o servidor de desenvolvimento:

```bash
make run
```

A API estará acessível em `http://127.0.0.1:8000`.
A documentação interativa (Swagger UI) pode ser acessada em `http://127.0.0.1:8000/docs`.

---

## 📂 Outros Desafios

Este repositório também contém soluções para desafios anteriores do bootcamp.

### Desafios do Projeto (Sistema Bancário)

Localizados na pasta `desafios do projeto/`:

- **Sistema Bancário V1 (`desafio1_solution.py`)**: Implementação procedural.
- **Sistema Bancário V2 (`desafio2_solution.py`)**: Implementação orientada a objetos.

### Desafios de Código (Lógica)

Localizados na pasta `desafios do código/`:

- Soluções para exercícios diversos de lógica de programação.