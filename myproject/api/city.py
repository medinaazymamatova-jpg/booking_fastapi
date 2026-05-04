from fastapi import HTTPException, Depends, APIRouter
from myproject.database.db import SessionLocal
from myproject.database.models import City
from myproject.database.schema import CitySchema
from sqlalchemy.orm import Session
from typing import List

city_router = APIRouter(prefix='/city', tags=['City CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@city_router.post('/', response_model=CitySchema)
async def create_city(city: CitySchema, db: Session = Depends(get_db)):
    city_db = City(**city.dict())
    db.add(city_db)
    db.commit()
    db.refresh(city_db)
    return city_db

@city_router.get('/', response_model=List[CitySchema])
async def list_city(db: Session = Depends(get_db)):
    return db.query(City).all()

@city_router.get('/{city_id}', response_model=CitySchema)
async def detail_city(city_id: int, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        raise HTTPException(detail='Мындай id жок', status_code=404)
    return city_db

@city_router.put('/{city_id}', response_model=dict)
async def update_city(city_id: int, city: CitySchema, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        raise HTTPException(detail='Мындай id жок', status_code=404)
    for city_key, city_value in city.dict().items():
        setattr(city_db, city_key, city_value)
    db.commit()
    db.refresh(city_db)
    return {'massage': 'City озгортулду'}

@city_router.delete('/{city_id')
async def delete_city(city_id: int, db: Session = Depends(get_db)):
    city_db = db.query(City).filter(City.id == city_id).first()
    if not city_db:
        raise HTTPException(detail='Мындай id жок', status_code=404)
    db.delete(city_db)
    db.commit()
    return {'massage': 'City очурулду'}

