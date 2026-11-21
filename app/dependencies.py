from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.security import decode_access_token

# Lê o cabeçalho "Authorization: Bearer <token>" e faz o botão Authorize do /docs pedir só o token.
# (O OAuth2PasswordBearer pedia usuário e senha em formulário, mas o /auth/login recebe JSON.)
# auto_error=False: a falta do token cai no mesmo 401 em português das demais falhas.
bearer_scheme = HTTPBearer(auto_error=False, description="Token recebido no login")

def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise unauthorized
    try:
        user_id = decode_access_token(credentials.credentials)
    except (InvalidTokenError, ValueError, KeyError):
        raise unauthorized
    user = db.get(User, user_id)
    if user is None:
        raise unauthorized
    return user
