from fastapi import HTTPException, Depends, APIRouter
from myproject.database.db import SessionLocal
from myproject.database.models import Country
from myproject.database.schema import CountrySchema
from sqlalchemy.orm import Session
from typing import List

country_router = APIRouter(prefix='/country', tags=['Country CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@country_router.post('/', response_model=CountrySchema)
async def create_country(country: CountrySchema, db: Session = Depends(get_db)):
    country_db = Country(**country.dict())
    db.add(country_db)
    db.commit()
    db.refresh(country_db)
    return country_db

@country_router.get('/', response_model=List[CountrySchema])
async def list_country(db: Session = Depends(get_db)):
    return db.query(Country).all()

@country_router.get('/{country_id}', response_model=CountrySchema)
async def detail_country(country_id: int, db: Session = Depends(get_db)):
    country_db = db.query(Country).filter(Country.id == country_id).first()
    if not country_db:
        raise HTTPException(detail='Мындай id жок', status_code=404)
    return country_db

@country_router.put('/{country_id}', response_model=dict)
async def update_country(country_id: int, country: CountrySchema, db: Session = Depends(get_db)):
    country_db = db.query(Country).filter(Country.id == country_id).first()
    if not country_db:
        raise HTTPException(detail='Мындай id жок', status_code=404)
    for country_key, country_value in country.dict().items():
        setattr(country_db, country_key, country_value)
    db.commit()
    db.refresh(country_db)
    return {'massage': 'Country озгортулду'}

@country_router.delete('/{country_id}')
async def delete_country(country_id = int, db: Session = Depends(get_db)):
    country_db = db.query(Country).filter(Country.id == country_id).first()
    if not country_db:
        raise HTTPException(detail='Мындай id жок', status_code=404)
    db.delete(country_db)
    db.commit()
    return {'massage': 'Country очурулду'}