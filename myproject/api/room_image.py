from fastapi import HTTPException, Depends, APIRouter
from myproject.database.db import SessionLocal
from sqlalchemy.orm import Session
from myproject.database.models import RoomImage
from myproject.database.schema import RoomImageSchema
from typing import List

room_image_router = APIRouter(prefix='/room_image', tags=['RoomImage CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@room_image_router.post('/', response_model=RoomImageSchema)
async def create_room_image(room_image: RoomImageSchema, db: Session = Depends(get_db)):
    room_image_db = RoomImage(**room_image.dict())
    db.add(room_image_db)
    db.commit()
    db.refresh(room_image_db)
    return room_image_db


@room_image_router.get('/', response_model=List[RoomImageSchema])
async def list_room_image(db: Session = Depends(get_db)):
    return db.query(RoomImage).all()

@room_image_router.get('/{room_image_id}', response_model=RoomImageSchema)
async def detail_room_image(room_image_id: int, db: Session = Depends(get_db)):
    room_image_db = db.query(RoomImage).filter(RoomImage.id == room_image_id).first()
    if not room_image_db:
        raise HTTPException(detail='Мындай id жок', status_code=404)
    return room_image_db

@room_image_router.put('/{room_image_id}', response_model=dict)
async def update_room_image(room_image_id: int, room_image: RoomImageSchema, db: Session = Depends(get_db)):
    room_image_db = db.query(RoomImage).filter(RoomImage.id == room_image_id).first()
    if not room_image_db:
        raise HTTPException(detail='Мындай id жок', status_code=404)
    for room_image_key, room_image_value in room_image.dict().items():
        setattr(room_image_db, room_image_key, room_image_value)
    db.commit()
    db.refresh(room_image_db)
    return {'massage': 'RoomImage update'}

@room_image_router.delete('/{room_image_id}')
async def delete_room_image(room_image_id: int, db: Session = Depends(get_db)):
    room_image_db = db.query(RoomImage).filter(RoomImage.id == room_image_id).first()
    if not room_image_db:
        raise HTTPException(detail='Мындай id жок', status_code=404)
    db.delete(room_image_db)
    db.commit()
    return {'massage': 'RoomImage delete'}