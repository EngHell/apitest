import aiohttp
import json
from enum import Enum
from typing import List, Any, Tuple
import asyncio
from fastapi import FastAPI, Response, status, HTTPException

from engines import get_itunes_results, get_tvmaze_results, get_people_results
from models import SearchSources, SearchResponse, SearchResult, ResultTypes

api = FastAPI()


async def process_results(itunes_code: int, itunes_results: any,
                          tvmaze_code: int, tvmaze_results: any,
                          people_code: int, people_results,
                          max_results_per_source=10) -> Tuple[bool, List[SearchResult]]:
    if not itunes_code == 200 and not tvmaze_code == 200 and not people_code == 200:
        return False, []

    final_results:[SearchResult] = []

    for i in range(0, max_results_per_source):
        if 0 <= i < len(itunes_results):
            found = itunes_results[i]

            title = found["trackName"]
            kind = found["kind"]
            description = f"By artist {found['artistName']} and of the collection {found['collectionName']}"
            url = found["previewUrl"]
            result = SearchResult(title=title,
                                  kind=kind,
                                  description=description,
                                  url=url
                                  )
            final_results.append(result)

    return True, final_results


async def get_results(q: str, mode: SearchSources) -> Tuple[bool, List[SearchResult]]:
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
    else:
        people_code = 200
        people_results = []

    success, results = await process_results(itunes_code, itunes_results,
                                       tvmaze_code, tvmaze_results,
                                       people_code, people_results)

    return success, results


@api.get("/", response_model=SearchResponse)
async def search(response: Response, q: str, mode: SearchSources = "all") -> SearchResponse:
    success, results = await get_results(q, mode)

    if not success:
        raise HTTPException(500,
                            detail="Internal server error o-o i know i should add more details here <3 but nope suffer for today.")

    final_result = SearchResponse(count=len(results), results=results)

    return final_result
