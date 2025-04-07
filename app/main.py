import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.endpoints import router as notification_router
from app.core.cache import init_cache
from app.core.database import get_db

app = FastAPI()

app.include_router(notification_router, prefix="/v1", tags=["notifications"])


@app.get("/ping_db")
async def ping_db(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    return {"status": "ok", "result": result.scalar()}


@app.on_event("startup")
async def startup():
    await init_cache()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
