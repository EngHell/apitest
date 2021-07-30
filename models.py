from enum import Enum
from typing import List, Literal

from pydantic import BaseModel, HttpUrl


class ResultTypes(str, Enum):
    people = "people"
    show = "show"
    book = "book"
    album = "album"
    coached_audio = "coached-audio"
    feature_movie = "feature-movie"
    interactive_booklet = "interactive-booklet"
    music_vide = "music-video"
    pdf = "pdf"
    podcast = "podcast"
    podcast_episode = "podcast-episode"
    software_package = "software-package"
    song = "song"
    tv_episode = "tv-episode"
    artist = "artist"


class Sources(str, Enum):
    itunes = "itunes"
    tvmaze = "tvmaze"
    people = "people"


class SearchResult(BaseModel):
    title: str
    kind: ResultTypes
    url: HttpUrl
    description: str
    sources: Sources


class SearchResponse(BaseModel):
    count: int
    results: List[SearchResult]


class SearchSources(str, Enum):
    itunes = "itunes"
    tvmaze = "tvmaze"
    people = "people"
    all = "all"