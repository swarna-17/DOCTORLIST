import sqlalchemy,databases
from fastapi import FastAPI
from pydantic import BaseModel,Field, main
#from sqlalchemy.sql.sqltypes import CHAR
from typing import List
from fastapi.middleware.cors import CORSMiddleware
## postgres database
DATABASE_URL = "postgresql://postgres:1234@127.0.0.1:5432/db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

doctors = sqlalchemy.Table(
    "doctors",
    metadata,
    sqlalchemy.Column("name" ,sqlalchemy.String,primary_key=True),
    sqlalchemy.Column("job" ,sqlalchemy.String),
    sqlalchemy.Column("country" ,sqlalchemy.String),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)


## Models
class doctorlist(BaseModel):
    name : str
    job : str
    country : str

class doctor(BaseModel):
    name : str

class doctorjob(BaseModel):
    name : str
    job : str

class doctorentry(BaseModel):
    name : str = Field(...,example="anc")
    job : str = Field(...,example="abcd")
    country : str = Field(...,example="abx")
    
'''
    class Config:
        orm_mode = True
'''

class doctorupdate(BaseModel):
    name : str = Field(...,example="Enter the doctor name")
    job : str = Field(...,example="abcd")
    country : str = Field(...,example="abx")
    

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/doctors",response_model=List[doctorlist])
async def find_doctors(search:str=""):
   # query_colmns='SELECT TOP 1* FROM DOCTORS'

   # var=database.fetch_all(query_colmns)
   # col_list=var.List()
   # col_list=(','.join(var))
    query = 'SELECT name,job,country FROM  DOCTORS '\
    "WHERE name like '%"+search+"%'"
    print(query)
    var= await database.fetch_all(query)
    return var 

@app.get("/doctors/{name}",response_model=List[doctor])
async def find_doctor_name(search:str=""):
    query = 'SELECT name FROM  DOCTORS '\
    "WHERE name like '%"+search+"%'"
    var= await database.fetch_all(query)
    return var

@app.get("/doctors/{name,job}",response_model=List[doctorjob])
async def find_doctor_name_job(search:str=""):
    query = 'SELECT name,job FROM DOCTORS'\
    "WHERE name like '%"+search+"%'"
    var=database.fetch_all(query)
    return await var 

@app.post("/doctors",response_model=doctorlist)
async def register_doctor(user: doctorentry):
    
    query = doctors.insert().values(
        name = user.name,
        job = user.job,
        country = user.country
        
    )

    await database.execute(query)
    return {
        
        **user.dict()
    }