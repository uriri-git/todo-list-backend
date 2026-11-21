from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from app.enums import StatusTarefa

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=180)
    description: str | None = None

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=180)
    description: str | None = None
    completed: bool | None = None
    status: StatusTarefa | None = None

    @field_validator("status")
    @classmethod
    def status_nao_pode_ser_nulo(cls, value):
        if value is None:
            raise ValueError("O status não pode ser nulo.")
        return value

class TaskOut(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    status: StatusTarefa
    owner_id: int
    created_at: datetime
    concluido_em: datetime | None = None
    model_config = ConfigDict(from_attributes=True)
