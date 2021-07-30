
import aiohttp
import json
from enum import Enum
from typing import List, Any, Tuple
import asyncio
from fastapi import FastAPI

from engines import get_itunes_results, get_tvmaze_results, get_people_results
from models import SearchSources
import xml.etree.ElementTree as ET

api = FastAPI()


async def get_results(q:str, mode:SearchSources):
    if mode == SearchSources.all or mode == SearchSources.itunes:
        itunes_code, itunes_results = await get_itunes_results(q)
    else:
        itunes_code = 200
        itunes_results = []

    if mode == SearchSources.all or mode == SearchSources.tvmaze:
        tvmaze_code, tvmaze_results = await get_tvmaze_results(q)
    else:
        tvmaze_code = 200
        tvmaze_results = []

    if mode == SearchSources.all or mode == SearchSources.personas:
        people_code, people_results = await get_people_results(q)

    return people_results


@api.get("/")
async def search(q: str, mode: SearchSources = "all"):
    results = await get_results(q, mode)
    return {"results": results}
