from datetime import date
from pydantic import BaseModel, EmailStr 
from enum import Enum
from fastapi import Form
 
 
class UserSchema(BaseModel):
    email: EmailStr
    username: str
    password: str
 
    class Config:
        from_attributes = True

 

    
    
   