import aiohttp
import json
from enum import Enum
from typing import List, Any, Tuple, Optional
import asyncio
from fastapi import FastAPI, Response, status, HTTPException, Query

from models import SearchSources, SearchResponse, SearchResult, ResultTypes
from results import get_results

api = FastAPI()


@api.get("/", response_model=SearchResponse)
async def search(
        q: str, mode: SearchSources = "all",
        max_results_per_source: Optional[int] = Query(10, ge=1, le=30)
    ) -> SearchResponse:
    success, results = await get_results(q, mode, max_results_per_source)

    if not success:
        raise HTTPException(500,
                            detail="Internal server error o-o i know i should add more details here <3 but nope suffer for today.")

    final_result = SearchResponse(count=len(results), results=results)

    return final_result
