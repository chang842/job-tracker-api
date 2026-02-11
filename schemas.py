from pydantic import BaseModel, Field

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

    class Config:
        orm_mode = True
