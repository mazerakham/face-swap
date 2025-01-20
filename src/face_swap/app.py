"""FastAPI application factory."""

import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .minimal_routes import router
from .dependencies import get_settings

# Load environment variables
load_dotenv()

# Print environment variables on startup
print("Environment variables:")
print(f"FACESWAP_API_KEY: {os.getenv('FACESWAP_API_KEY')}")
print(f"AWS_ACCESS_KEY_ID: {os.getenv('AWS_ACCESS_KEY_ID')}")
print(f"AWS_SECRET_ACCESS_KEY: {os.getenv('AWS_SECRET_ACCESS_KEY')}")
print(f"S3_BUCKET: {os.getenv('S3_BUCKET')}")

app = FastAPI(title="Face Swap API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1", dependencies=[Depends(get_settings)])
