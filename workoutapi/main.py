from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination
from sqlalchemy.exc import IntegrityError
from workoutapi.routers import api_router

app = FastAPI(title='WorkoutApi')

@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=303,
        content={"detail": "Já existe um atleta cadastrado com o cpf: x"}
    )

app.include_router(api_router)
add_pagination(app)