from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import Base, engine
from app.routers import auth, tasks, users

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TODO LIST API",
    description=(
        "API de lista de tarefas. Para usar as rotas protegidas: faça login em POST /auth/login, "
        "copie o access_token e cole no botão **Authorize**."
    ),
    version="1.0.0",
)

# Sem o CORS, o navegador bloqueia o front-end (outro endereço) de ler as respostas da API.
# O expose_headers libera o JavaScript para ler o X-Total-Count; sem ele, a paginação do front ficaria cega.
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.origens_permitidas),
    allow_credentials=False,  # o token vai no cabeçalho Authorization, não em cookie
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)

@app.get("/", tags=["Início"])
def home():
    return {"message": "TODO LIST API no ar"}
