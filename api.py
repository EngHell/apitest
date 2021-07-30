
import aiohttp
import json
from enum import Enum
from typing import List, Any, Tuple
import asyncio
from fastapi import FastAPI
from models import SearchSources

api = FastAPI()


async def get_itunes_results(q: str) -> Tuple[int, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://itunes.apple.com/search?term={q}") as resp:
            code = resp.status
            data = await resp.read()

    if code == 200:
        results = json.loads(data)
    else:
        results = data

    return code, results


async def get_tvmaze_results(q: str) -> Tuple[int, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.tvmaze.com/search/shows?q={q}") as resp:
            code = resp.status

            if code == 200:
                results = await resp.json()
            else:
                results = await resp.read()

    return code, results


async def get_results(q:str, mode:SearchSources):

    if mode == SearchSources.all or mode == SearchSources.itunes:
        itunes_code, itunes_results = await get_itunes_results(q)
    else:
        itunes_code = 200,
        itunes_results = []

    if mode == SearchSources.all or mode == SearchSources.tvmaze:
        tvmaze_code, tvmaze_results = await get_tvmaze_results(q)

    return tvmaze_results


@api.get("/")
async def search(q: str, mode: SearchSources = "all"):
    results = await get_results(q, mode)
    return {"results": results}
