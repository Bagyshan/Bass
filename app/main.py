from fastapi import FastAPI
from app.users import routers as users_routers
app = FastAPI()

app.include_router(users_routers.router)