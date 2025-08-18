from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
allowed_roles = ["user", "admin", "dealer"]
class UserRegister(BaseModel):
    username:str = Field(..., min_length=3, max_length=20)
    email : EmailStr
    password:str = Field(..., min_length=6, max_length=60)
    role:str 
    @validator('role')
    def validate_role(cls, v):
        if v not in allowed_roles:
            raise ValueError(f"Role must be one of {allowed_roles}")
        return v
class UserLogin(BaseModel):
    email: EmailStr
    password:str
class UserResponse(BaseModel):
    id:str
    username:str
    email:EmailStr
    role:str
class TokenData(BaseModel):
    access_token : str
    token_type:str='Bearer'
class UserUpdate(BaseModel):
    username: Optional[str]
    password: Optional[str]
    address: Optional[str]
    phone: Optional[str] = Field(None, min_length=10, max_length=10)