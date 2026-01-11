import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Path, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from enum import Enum

# --- Configuration ---
SECRET_KEY = "sua_chave_secreta_super_segura" # Em produção, use env vars
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(
    title="Desafio 3: API Bancária Assíncrona",
    description="API para gestão de contas e transações bancárias com autenticação JWT.",
    version="1.0.0"
)

# --- Security & Auth Setup ---
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Domain Models (Pydantic) ---

class TipoTransacao(str, Enum):
    DEPOSITO = "deposito"
    SAQUE = "saque"

class TransacaoBase(BaseModel):
    valor: float = Field(..., gt=0, description="O valor deve ser positivo")

class TransacaoCreate(TransacaoBase):
    tipo: TipoTransacao

class TransacaoResponse(TransacaoBase):
    tipo: TipoTransacao
    data: datetime

class ExtratoResponse(BaseModel):
    saldo: float
    transacoes: List[TransacaoResponse]

class UserBase(BaseModel):
    username: str # CPF
    nome: str
    email: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., max_length=72, description="Senha do usuário (máx 72 caracteres)")
    data_nascimento: str

class UserResponse(UserBase):
    data_nascimento: str
    numero_conta: int

class Token(BaseModel):
    access_token: str
    token_type: str

# --- In-Memory Database Simulation ---
# Structure:
# users_db: { "cpf": { data... } }
# accounts_db: { "account_number": { balance: float, transactions: [], user_cpf: str } }
# simplified: 1 user = 1 account for this challenge context (or 1 user -> N accounts, but lets stick to 1:1 for simplicity unless requested otherwise. Desafio 2 allowed multiple, so I'll link by CPF)

fake_users_db = {}
fake_accounts_db = {} # Key: account_number (int)

# --- Helper Classes (Domain Logic) ---

class ContaSistema:
    def __init__(self, numero: int, cpf_titular: str):
        self.numero = numero
        self.cpf_titular = cpf_titular
        self.saldo = 0.0
        self.transacoes = [] # List of dicts

    def depositar(self, valor: float):
        if valor <= 0:
            raise ValueError("Valor deve ser positivo")
        self.saldo += valor
        self.transacoes.append({
            "tipo": TipoTransacao.DEPOSITO,
            "valor": valor,
            "data": datetime.now()
        })
        return True

    def sacar(self, valor: float):
        if valor <= 0:
            raise ValueError("Valor deve ser positivo")
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente")
        self.saldo -= valor
        self.transacoes.append({
            "tipo": TipoTransacao.SAQUE,
            "valor": valor,
            "data": datetime.now()
        })
        return True

# Initialize some data
# (Account database will store ContaSistema objects)

# --- Dependencies ---

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception
    return user

async def get_account_by_id(numero_conta: int = Path(..., title="Número da Conta")):
    if numero_conta not in fake_accounts_db:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return fake_accounts_db[numero_conta]

# --- Endpoints ---

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/usuarios", response_model=UserResponse, status_code=201)
async def criar_usuario(user: UserCreate):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="CPF já cadastrado")
    
    try:
        hashed_password = get_password_hash(user.password)
    except ValueError:
        raise HTTPException(status_code=400, detail="Senha inválida ou muito longa (max 72 chars).")
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]
    
    fake_users_db[user.username] = user_dict
    
    # Auto-create account (simplification akin to desafio 2)
    numero_conta = len(fake_accounts_db) + 1
    nova_conta = ContaSistema(numero=numero_conta, cpf_titular=user.username)
    fake_accounts_db[numero_conta] = nova_conta
    
    return {**user.dict(), "numero_conta": numero_conta}

@app.post("/contas/{numero_conta}/transacoes", response_model=TransacaoResponse)
async def realizar_transacao(
    transacao: TransacaoCreate,
    conta: ContaSistema = Depends(get_account_by_id),
    current_user: dict = Depends(get_current_user)
):
    # Verify ownership
    if conta.cpf_titular != current_user["username"]:
        raise HTTPException(status_code=403, detail="Acesso negado a esta conta")

    try:
        if transacao.tipo == TipoTransacao.DEPOSITO:
            conta.depositar(transacao.valor)
        elif transacao.tipo == TipoTransacao.SAQUE:
            conta.sacar(transacao.valor)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    return {
        "tipo": transacao.tipo,
        "valor": transacao.valor,
        "data": conta.transacoes[-1]["data"]
    }

@app.get("/contas/{numero_conta}/extrato", response_model=ExtratoResponse)
async def ver_extrato(
    numero_conta: int,
    conta: ContaSistema = Depends(get_account_by_id),
    current_user: dict = Depends(get_current_user)
):
    if conta.cpf_titular != current_user["username"]:
        raise HTTPException(status_code=403, detail="Acesso negado a esta conta")
        
    return {
        "saldo": conta.saldo,
        "transacoes": conta.transacoes
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
