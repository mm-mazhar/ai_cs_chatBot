# -*- coding: utf-8 -*-
# """
# desc.py
# Created on Nov 29, 2024
# @ Author: Mazhar
# """

from typing import Any

from configs import cfg
from fastapi import APIRouter, status
from loguru import logger
from schemas import Desc

desc_router = APIRouter(tags=[cfg.ROUTES.DESC_TAG])


# GET API DESCRIPTION
@desc_router.get(
    cfg.ROUTES.DESCRIPTION, response_model=Desc, status_code=status.HTTP_200_OK
)
def description() -> Desc:
    """API Description/Project information.

    Returns:
        schemas.Desc: desc
    """
    desc: Any = Desc(
        name=cfg.VERSION.API_PROJECT_NAME,
        api_version=cfg.VERSION.VER,
        package_version=cfg.VERSION.PACKAGE_VERSION,
    )
    logger.info(f"API Description: {desc}")
    return desc
