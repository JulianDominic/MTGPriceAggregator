import os
from litestar.config.cors import CORSConfig

HOST_IP = os.environ.get("HOST_IP", "localhost")
FRONTEND_URL = f"http://frontend:10015"
ORIGINS = [FRONTEND_URL, "http://localhost:10015"]
HEADERS = [
    "Accept",
    "Accept-Language", 
    "Accept-Encoding",
    "Content-Type",
    "DNT",
    "Origin",
    "Referer",
    "Sec-Fetch-Dest",
    "Sec-Fetch-Mode",
    "Sec-Fetch-Site",
    "User-Agent",
]

class MTGCORSConfig(CORSConfig):
    allow_origins=ORIGINS
    allow_methods=["GET", "OPTIONS"]
    allow_headers=HEADERS
