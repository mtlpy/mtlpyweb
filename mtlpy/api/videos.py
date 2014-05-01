import requests
import arrow


def _sort_video(a, b):
    return (cmp(arrow.get(a["published"]["$t"]), arrow.get(b["published"]["$t"]))
            * -1)


def get_all_videos(url):
    content = requests.get(url=url).json()
    elements = sorted(content["feed"]["entry"], _sort_video)
    for i, el in enumerate(elements):
        for k in elements[i]:
            if "$t" in  elements[i][k]:
                elements[i][k] = elements[i][k]["$t"]
            if k == "published":
                elements[i][k] = arrow.get(elements[i][k])
            if k == "id":
                elements[i][k] = elements[i][k].split(":")[-1]
    return elements
