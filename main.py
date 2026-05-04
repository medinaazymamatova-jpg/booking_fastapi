import uvicorn
from fastapi import FastAPI
from myproject.api.user import user_router
from myproject.api.country import country_router
from myproject.api.city import city_router
from myproject.api.service import service_router
from myproject.api.hotel import hotel_router
from myproject.api.hotel_image import hotel_image_router
from myproject.api.room import room_router
from myproject.api.room_image import room_image_router
from myproject.api.review import review_router
from myproject.api.booking import booking_router
from myproject.api.auth import auth_router
from myproject.admin.setup import setup_admin


booking_app = FastAPI()

booking_app.include_router(auth_router)
booking_app.include_router(user_router)
booking_app.include_router(country_router)
booking_app.include_router(city_router)
booking_app.include_router(service_router)
booking_app.include_router(hotel_router)
booking_app.include_router(hotel_image_router)
booking_app.include_router(room_router)
booking_app.include_router(room_image_router)
booking_app.include_router(booking_router)
booking_app.include_router(review_router)
setup_admin(booking_app)

if __name__ == '__main__':
    uvicorn.run(booking_app, host='127.0.0.1', port=8000)