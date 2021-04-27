import uvicorn
from fastapi import FastAPI

from app.routing import router

app = FastAPI()

app.include_router(router, prefix='/tasks', tags=['tasks'])

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
