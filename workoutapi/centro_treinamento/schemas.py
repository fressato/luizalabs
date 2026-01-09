from typing import Annotated
from pydantic import Field
from workoutapi.contrib.schemas import BaseSchema


class CentroTreinamento(BaseSchema):
    nome: Annotated[str, Field(description="Nome do centro de treinamento", example="CT King", max_length=20)]
    endereco: Annotated[str, Field(description="Endereço do centro de treinamento", example="Rua dos Treinadores, 123", max_length=60)]
    proprietario: Annotated[str, Field(description="Proprietário do centro de treinamento", example="John", max_length=30)]