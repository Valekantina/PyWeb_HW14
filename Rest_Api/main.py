import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from src.config.config import settings
from src.routes import auth, contacts, users

app = FastAPI()

app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/api')


@app.on_event('startup')
async def startup():
    """
    The startup function is called when the application starts up.
    It's a good place to initialize things that are needed by your app, such as database connections or caches.
    
    :return: A coroutine, so we need to wrap it in asyncio
    :doc-author: Trelent
    """
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding='utf-8', decode_responses=True)
    await FastAPILimiter.init(r)

origins = ['http://localhost:3000']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/')
def read_root():
    """
    The read_root function is a view function that returns the root of the API.
    It's purpose is to provide a welcome message for users who visit this endpoint.
    
    :return: A dictionary
    :doc-author: Trelent
    """
    return {'message': 'Welcome to Contacts App!'}


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
