from enum import Enum


class SearchSources(str, Enum):
    itunes = "itunes"
    tvmaze = "tvmaze"
    personas = "personas"
    all = "all"