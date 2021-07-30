from typing import Tuple, List

from engines import get_itunes_results, get_tvmaze_results, get_people_results

from models import SearchSources, SearchResponse, SearchResult, ResultTypes


async def process_results(itunes_code: int, itunes_results: any,
                          tvmaze_code: int, tvmaze_results: any,
                          people_code: int, people_results,
                          max_results_per_source) -> Tuple[bool, List[SearchResult]]:
    if not itunes_code == 200 and not tvmaze_code == 200 and not people_code == 200:
        return False, []

    final_results:[SearchResult] = []

    for i in range(0, max_results_per_source):
        if 0 <= i < len(itunes_results):
            found = itunes_results[i]

            if "trackName" in found:
                title = found["trackName"]
            elif "collectionName" in found:
                title = found["collectionName"]
            else:
                title = "not name found."
            if "kind" in found:
                kind = found["kind"]
            else:
                kind = found["wrapperType"]

            description = f"By artist {found['artistName']}"
            url = found["previewUrl"]
            result = SearchResult(title=title,
                                  kind=kind,
                                  description=description,
                                  url=url,
                                  source="itunes"
                                  )
            final_results.append(result)

        if 0 <= i < len(tvmaze_results):
            found = tvmaze_results[i]["show"]
            title = found["name"]
            kind = "show"
            description = f"{found['type']} - {found['status']} premiered on {found['premiered']}\n\n" \
                          f"{found['summary']}"
            url = found["url"]
            result = SearchResult(title=title, kind=kind, description=description, url=url, source="tvmaze")
            final_results.append(result)

        if 0 <= i < len(people_results):
            found = people_results[i]
            result = SearchResult(title=found["title"],
                                  kind="people",
                                  description=found["description"],
                                  source="people")
            final_results.append(result)

    return True, final_results


async def get_results(q: str, mode: SearchSources, max_results_per_source) -> Tuple[bool, List[SearchResult]]:
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
                                       people_code, people_results, max_results_per_source)

    return success, results