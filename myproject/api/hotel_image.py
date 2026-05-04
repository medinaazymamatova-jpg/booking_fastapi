from fastapi import HTTPException, Depends, APIRouter
from myproject.database.db import SessionLocal
from myproject.database.models import HotelImage
from myproject.database.schema import HotelImageSchema
from sqlalchemy.orm import Session
from typing import List

hotel_image_router = APIRouter(prefix='/hotel_image',tags= ['HotelImage CRUD'] )

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@hotel_image_router.post('/', response_model=HotelImageSchema)
async def create_hotel_image(hotel: HotelImageSchema, db: Session = Depends(get_db)):
    hotel_image_db = HotelImage(**hotel.dict())
    db.add(hotel_image_db)
    db.commit()
    db.refresh(hotel_image_db)
    return hotel_image_db

@hotel_image_router.get('/', response_model=List[HotelImageSchema])
async def list_hotel_image(db: Session = Depends(get_db)):
    return db.query(HotelImage).all()

@hotel_image_router.get('/{hotel_image_id}', response_model=HotelImageSchema)
async def detail_hotel_image(hotel_image_id: int, db: Session = Depends(get_db)):
    hotel_image_db = db.query(HotelImage).filter(HotelImage.id == hotel_image_id).first()
    if not hotel_image_db:
        raise HTTPException(detail='Мындай id жок', status_code=404)
    return hotel_image_db

@hotel_image_router.put('/{hotel_image_id}', response_model=dict)
async def update_hotel_image(hotel_image_id: int, hotel_image: HotelImageSchema, db: Session = Depends(get_db)):
    hotel_image_db = db.query(HotelImage).filter(HotelImage.id == hotel_image_id).first()
    if not hotel_image_db:
        raise HTTPException(detail='Мындай id жок', status_code=404)
    for hotel_image_key, hotel_image_value in hotel_image.dict().items():
        setattr(hotel_image_db, hotel_image_key, hotel_image_value)
    db.commit()
    db.refresh(hotel_image_db)
    return {'massage': 'HotelImage озгортулду'}

@hotel_image_router.delete('/{hotel_image_id}')
async def delete_hotel_image(hotel_image_id: int, db: Session = Depends(get_db)):
    hotel_image_db = db.query(HotelImage).filter(HotelImage.id == hotel_image_id).first()
    if not hotel_image_db:
        raise HTTPException(detail='Мындай id жок', status_code=404)
    db.delete(hotel_image_db)
    db.commit()
    return {'massage': 'HotelImage очурулду'}