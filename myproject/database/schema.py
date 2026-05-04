from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime
from .models import Room_Type, Room_Status, Role_Choices

class CountrySchema(BaseModel):
    id: int
    country_name: str
    country_image: str

class UserProfileInputSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    phone_number: str
    age: Optional[int]
    user_image: Optional[str]
    role: Role_Choices
    country_id: int

class UserProfileOutSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    phone_number: str
    age: Optional[int]
    user_image: Optional[str]
    role: Role_Choices
    date_register: datetime
    country_id: int


class UserProfileLoginSchema(BaseModel):
    email: EmailStr
    password: str


class CitySchema(BaseModel):
    id:int
    city_name: str
    city_image: str
    countries_id: int

class ServiceSchema(BaseModel):
    id: int
    service_name: str
    service_image: str

class HotelSchema(BaseModel):
    id:int
    hotel_name: str
    hotel_stars: Optional[int]
    street: str
    postal_index: int
    description: str
    country_id: int
    service_id: int
    owner_id: int

class HotelImageSchema(BaseModel):
    id: int
    hotel_image: str
    hotel_id: int

class RoomInputSchema(BaseModel):
    room_number:int
    room_type: Room_Type
    room_status: Room_Status
    price: int
    room_description: str
    max_guest: int
    hotel_id: int


class RoomOutSchema(BaseModel):
    id:int
    room_number:int
    room_type: Room_Type
    room_status: Room_Status
    price: int
    room_description: str
    max_guest: int
    hotel_id: int

class RoomImageSchema(BaseModel):
    id:int
    room_image: str
    room_id: int

class BookingInputSchema(BaseModel):
    check_in: date
    check_out: date
    hotel_id: int
    room_id: int
    user_id: int

class BookingOutSchema(BaseModel):
    id: int
    check_in: date
    check_out: date
    created_date: datetime
    hotel_id: int
    room_id: int
    user_id: int

class ReviewInputSchema(BaseModel):
    hotel_id: int
    user_id: int
    text: str
    rating: int


class ReviewOutSchema(BaseModel):
    id:int
    hotel_id: int
    user_id: int
    text: str
    rating: int
    created_date: datetime