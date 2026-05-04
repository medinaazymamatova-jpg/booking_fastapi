from .views import (UserProfileAdmin, CountryAdmin, CityAdmin, ServiceAdmin,
                     HotelAdmin, HotelImageAdmin, RoomAdmin, RoomImageAdmin, ReviewAdmin, BookingAdmin)
from fastapi import FastAPI
from sqladmin import Admin
from myproject.database.db import engine

def setup_admin(booking_app: FastAPI):
    admin = Admin(booking_app, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(CountryAdmin)
    admin.add_view(CityAdmin)
    admin.add_view(ServiceAdmin)
    admin.add_view(HotelAdmin)
    admin.add_view(HotelImageAdmin)
    admin.add_view(RoomAdmin)
    admin.add_view(RoomImageAdmin)
    admin.add_view(BookingAdmin)
    admin.add_view(ReviewAdmin)