import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from routers.b2b_seller import router

app = FastAPI()

app.include_router(router=router)


@app.get("/")
async def root():
    return {"message": "B2B Mock Seller!!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
