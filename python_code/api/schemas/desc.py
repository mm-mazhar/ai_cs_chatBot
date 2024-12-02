# -*- coding: utf-8 -*-
# """
# desc.py
# Created on Nov 29, 2024
# @ Author: Mazhar
# """

from pydantic import BaseModel


class Desc(BaseModel):
    name: str
    api_version: str
    package_version: str
