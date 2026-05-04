from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, SmallInteger, Enum, ForeignKey, DateTime, Text, Date
from .db import Base
from typing import Optional, List
from enum import Enum as PyEnum
from datetime import date, datetime

class Country(Base):
    __tablename__ = 'country'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    country_name: Mapped[str] = mapped_column(String(64), unique=True)
    country_image: Mapped[str] = mapped_column(String)

    country_user: Mapped[List['UserProfile']] = relationship(back_populates='country',
                                                             cascade='all, delete-orphan')
    country_city:Mapped[List['City']] = relationship(back_populates='countries',
                                                        cascade='all, delete-orphan')
    hotel_country:Mapped[List['Hotel']] = relationship(back_populates='country_hotel',
                                                        cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.country_name}'


class Role_Choices(str, PyEnum):
    client = 'client'
    owner = 'owner'


class UserProfile(Base):
    __tablename__ = 'profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(34), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(34), nullable=True)
    username: Mapped[str] = mapped_column(String(34), unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String(34))
    phone_number: Mapped[str] = mapped_column(String)
    age: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    user_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[Role_Choices] = mapped_column(Enum(Role_Choices), default=Role_Choices.client)
    country_id: Mapped[int] = mapped_column(ForeignKey('country.id'))
    country: Mapped[Country] = relationship(back_populates='country_user')
    date_register: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    hotel_owner: Mapped[List['Hotel']] = relationship(back_populates='owner',
                                                     cascade='all, delete-orphan')
    user_booking: Mapped[List['Booking']] = relationship(back_populates='user',
                                                         cascade='all, delete-orphan')
    user_review:  Mapped[List['Review']] =  relationship(back_populates='user_review',
                                                     cascade='all, delete-orphan')

    refresh_user: Mapped[List['RefreshToken']] = relationship(back_populates='users',
                                                              cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.first_name}, {self.last_name}'

class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    users_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    users: Mapped[UserProfile] = relationship(back_populates='refresh_user')
    token: Mapped[str] = mapped_column(String, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city_name: Mapped[str] = mapped_column(String(43), unique=True)
    city_image: Mapped[str] = mapped_column(String)

    countries_id: Mapped[int] = mapped_column(ForeignKey('country.id'))
    countries: Mapped[Country] = relationship(back_populates='country_city')

    city_hotel: Mapped[List['Hotel']] = relationship(back_populates='city',
                                                     cascade='all, delete-orphan')
    def __repr__(self):
        return f'{self.city_name}'

class Service(Base):
    __tablename__ = 'service'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    service_name: Mapped[str] = mapped_column(String(32), unique=True)
    service_image: Mapped[str] = mapped_column(String)

    service_hotel: Mapped[List['Hotel']] = relationship(back_populates='service',
                                                     cascade='all, delete-orphan')
    def __repr__(self):
        return f'{self.service_name}'

class Hotel(Base):
    __tablename__ = 'hotel'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_name: Mapped[str] = mapped_column(String(100))
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    city: Mapped[City] = relationship(back_populates='city_hotel')
    country_id: Mapped[int] = mapped_column(ForeignKey('country.id'))
    country_hotel: Mapped[Country] = relationship(back_populates='hotel_country')
    hotel_stars: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    street: Mapped[str] = mapped_column(String(100))
    postal_index: Mapped[int] = mapped_column(Integer)
    service_id: Mapped[int] = mapped_column(ForeignKey('service.id'))
    service: Mapped[Service] = relationship(back_populates='service_hotel')
    description: Mapped[str] = mapped_column(Text)
    owner_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    owner: Mapped[UserProfile] = relationship(back_populates='hotel_owner')

    hotel_image: Mapped[List['HotelImage']] = relationship(back_populates='hotel',
                                                     cascade='all, delete-orphan')
    room_hotel: Mapped[List['Room']] = relationship(back_populates='hotel_room',
                                                     cascade='all, delete-orphan')
    hotel_booking: Mapped[List['Booking']] =  relationship(back_populates='hotel_booking',
                                                     cascade='all, delete-orphan')
    hotel_review:  Mapped[List['Review']] =  relationship(back_populates='hotel_review',
                                                     cascade='all, delete-orphan')
    def __repr__(self):
        return f'{self.hotel_name}, {self.hotel_stars}'

class HotelImage(Base):
    __tablename__ = 'hotel_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_image: Mapped[str] = mapped_column(String)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    hotel: Mapped[Hotel] = relationship(back_populates='hotel_image')

    def __repr__(self):
        return f'{self.hotel_image}'

class Room_Type(str, PyEnum):
    luxury = 'luxury'
    junior_suite = "junior_suite"
    economy = "economy"
    family = "family"
    single = "single"
    double = "double"

class Room_Status(str, PyEnum):
    available = 'available'
    booked = 'booked'
    occupied = 'occupied'


class Room(Base):
    __tablename__ = 'room'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    hotel_room: Mapped[Hotel] = relationship(back_populates='room_hotel')
    room_number: Mapped[int] = mapped_column(SmallInteger, unique=True)
    room_type: Mapped[Room_Type] = mapped_column(Enum(Room_Type), default=Room_Type.economy)
    room_status: Mapped[Room_Status] = mapped_column(Enum(Room_Status))
    price: Mapped[int] = mapped_column(Integer)
    room_description: Mapped[str] = mapped_column(Text)
    max_guest: Mapped[int] = mapped_column(SmallInteger)

    room_image: Mapped[List['RoomImage']] = relationship(back_populates='room',
                                                         cascade='all, delete-orphan')
    room_booking:Mapped[List['Booking']] = relationship(back_populates='room_booking',
                                                         cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.room_number}, {self.price}'


class RoomImage(Base):
    __tablename__ = 'room_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    room_image: Mapped[str] = mapped_column(String)
    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    room: Mapped[Room] = relationship(back_populates='room_image')

    def __repr__(self):
        return f'{self.room_image}'

class Booking(Base):
    __tablename__ = 'booking'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    hotel_booking: Mapped[Hotel] = relationship(back_populates='hotel_booking')
    room_id: Mapped[int] = mapped_column(ForeignKey('room.id'))
    room_booking: Mapped[Room] = relationship(back_populates='room_booking')
    user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    user: Mapped[UserProfile] = relationship(back_populates='user_booking')
    check_in: Mapped[date] = mapped_column(Date)
    check_out:  Mapped[date] = mapped_column(Date)
    created_date: Mapped[datetime] = mapped_column(DateTime, autoincrement=True, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.check_in} {self.check_out}'

class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotel.id'))
    hotel_review: Mapped[Hotel] = relationship(back_populates='hotel_review')
    user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    user_review: Mapped[UserProfile] = relationship(back_populates='user_review')
    text: Mapped[str] = mapped_column(Text)
    rating: Mapped[int] = mapped_column(SmallInteger)
    created_date: Mapped[datetime] = mapped_column(DateTime, autoincrement=True, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.rating}'