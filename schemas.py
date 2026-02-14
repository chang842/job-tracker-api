from pydantic import BaseModel, Field, EmailStr


# ---------- Auth ----------
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=60)


from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=60)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=60)

class UserPublic(BaseModel):
    id: str
    email: EmailStr



class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Jobs ----------
class JobBase(BaseModel):
    company: str = Field(min_length=1, max_length=100)
    position: str = Field(min_length=1, max_length=120)
    status: str = Field(min_length=1, max_length=40)


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    status: str = Field(min_length=1, max_length=40)


class JobResponse(JobBase):
    id: str
    user_id: str

    class Config:
        from_attributes = True  # pydantic v2
