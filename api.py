import aiohttp
import json
from enum import Enum
from typing import List, Any, Tuple, Optional
import asyncio
from fastapi import FastAPI, Response, status, HTTPException, Query, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models import SearchSources, SearchResponse, SearchResult, ResultTypes, User, UserInDB
from results import get_results

api = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_decode_token(token):
    return User(
        username=token+"fakedecoded", email="john@example.com", fullname="John doe"
    )

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

def fake_hash_password(password: str):
    return "fakehashed" + password


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



@api.get("/", response_model=SearchResponse)
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


@api.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

@api.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
