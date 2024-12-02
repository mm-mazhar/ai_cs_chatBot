# -*- coding: utf-8 -*-
# """
# main.py
# Created on Nov 27, 2024
# @ Author: Mazhar
# """


from typing import Any

from configs import cfg, settings, setup_logging
from fastapi import APIRouter, FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import HTMLResponse
from loguru import logger
from routers import desc_router, order_taking_router

# setup logging as early as possible
setup_logging(config=settings)

# Prefix for all API endpoints
preFix: str = cfg.VERSION.API_V1_STR

# print(f"preFix: {preFix}")
# print(f" Type of preFix: {type(preFix)}")

app = FastAPI(
    title=f"{cfg.VERSION.API_PROJECT_NAME}",
    openapi_url=f"{preFix}/openapi.json",
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
    servers=settings.SERVERS,
)

# models.Base.metadata.create_all(bind=engine)


root_router = APIRouter(tags=["Root"])


@root_router.get("/")
def index(request: Request) -> Any:
    """Basic HTML response."""
    body: str = (
        "<html>"
        "<body style='display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #7d8492;'>"
        "<div style='text-align: center; background-color: white; padding: 20px; border-radius: 20px;'>"
        f"<h1 style='font-weight: bold; font-family: Arial;'>{cfg.VERSION.API_PROJECT_NAME}</h1>"
        f"<h3 style='font-weight: bold; font-family: Arial;'>Version: {cfg.VERSION.VER}</h3>"
        "<div>"
        f"<h4>Check the docs: <a href='/docs'>here</a><h4>"
        "</div>"
        "</div>"
        "</body>"
        "</html>"
    )

    return HTMLResponse(content=body)


app.include_router(root_router)
app.include_router(desc_router, prefix=preFix)
app.include_router(order_taking_router, prefix=preFix)


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# # For Production Deployment
# # Add TrustedHost middleware
# app.add_middleware(
#     TrustedHostMiddleware,
#     allowed_hosts=["*.app", "*.example.com"],
# )

# # Add GZip middleware
# app.add_middleware(
#     GZipMiddleware,
#     minimum_size=1000,
# )

if __name__ == "__main__":
    # Use this for debugging purposes only
    logger.warning("Running in development mode. Do not run like this in production.")
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8001, log_level="debug", reload=True)
