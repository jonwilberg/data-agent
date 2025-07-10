"""FastAPI application for Census Data Agent."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from api.routes import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Census Data Agent API",
    description="API for querying census data using natural language",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting Census Data Agent API")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Census Data Agent API")