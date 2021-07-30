import aiohttp
import json
from enum import Enum
from typing import List, Any, Tuple, Optional
from datetime import datetime, timedelta
import asyncio
from fastapi import FastAPI, Response, status, HTTPException, Query, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from auth import oauth2_scheme, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, \
    get_current_active_user
from db import fake_users_db
from models import SearchSources, SearchResponse, SearchResult, ResultTypes, User, UserInDB, TokenData, Token
from results import get_results


app = FastAPI()


@app.get("/", response_model=SearchResponse)
async def search(
        q: str, mode: SearchSources = "all",
        max_results_per_source: Optional[int] = Query(10, ge=1, le=30),
        token: str = Depends(oauth2_scheme)
    ) -> SearchResponse:
    success, results = await get_results(q, mode, max_results_per_source)

    if not success:
        raise HTTPException(500,
                            detail="Internal server error o-o i know i should add more details here <3 but nope suffer for today.")

    final_result = SearchResponse(count=len(results), results=results)

    return final_result


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
