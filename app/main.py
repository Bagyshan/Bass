from fastapi import FastAPI
from app.users import routers as users_routers
from app.posts import routers as posts_routers

app = FastAPI()

@app.get("/")

async def root():
    return {"message": "Hello World"}

app.include_router(users_routers.router)
app.include_router(posts_routers.router)