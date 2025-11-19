from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Callable
from contextlib import asynccontextmanager


from src.database import create_tables, delete_tables
from src.api import main_router
from src.models.request_logs import RequestLogsModel
from src.database import new_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await delete_tables()
    # print('База данных очищена')
    await create_tables()
    print('База данных готова к работе')
    yield
    print('Завершение')

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

app.include_router(main_router)

@app.middleware('http')
async def log_request(request: Request, call_next: Callable):
    response = await call_next(request)
    async with new_session() as session:
        log = RequestLogsModel(
        time = datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        method = request.method,
        url = str(request.url)
    )
        session.add(log)
        await session.commit()
    # if 'uid' not in request.cookies:
    #     print(request.cookies['uid'])
    return response