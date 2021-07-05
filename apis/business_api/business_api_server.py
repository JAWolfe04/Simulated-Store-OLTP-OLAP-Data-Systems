from fastapi import FastAPI

from apis.business_api.api.api_router import api_router

app = FastAPI()

app.include_router(api_router, prefix = "/v1")

@app.get("/")
async def root():
    return {"message": "This is the API for Simulated Superstore Data System"}
