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


async def get_people_results(q: str) -> Tuple[int, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://www.crcind.com/csp/samples/SOAP.Demo.cls?soap_method=GetByName&name={q}") as resp:
            code = resp.status

            data = await resp.read()

            if code == 200:
                root = ET.fromstring(data)
                list_by_name = root.find(".//ListByName")
                children = list_by_name
                results = []
                for child in children:
                    id = child[0].text
                    name = child[1].text
                    dob = child[2].text
                    ssn = child[3].text

                    results.append({
                        "title": name,
                        "link": None,
                        "description": f"Birthed on {dob}, with an ssn of {ssn}"
                    })
            else:
                results = await resp.read()

    return code, results