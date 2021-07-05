from fastapi import APIRouter

from apis.business_api.api.endpoints import users

api_router = APIRouter()
api_router.include_router(users.router, prefix = "/users", tags = ["users"])
