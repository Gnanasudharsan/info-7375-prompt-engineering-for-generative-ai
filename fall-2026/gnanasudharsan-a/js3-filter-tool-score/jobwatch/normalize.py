"""Map Greenhouse, Ashby and Lever postings to the fields jobwatch/rule.py reads.

Output keys: id, title, content, location {"name"}, departments [{"name"}],
updated_at, absolute_url, source_ats. A field the source lacks becomes None;
no value is invented. Shapes follow each ATS's public job-board API.
"""

LOCATION_SEPARATOR = " | "  # rule.py splits location.name on "|" and ";"


def _str_or_none(value):
    return value if isinstance(value, str) and value.strip() else None


def _location(names):
    names = [n for n in (_str_or_none(x) for x in names) if n]
    # Keep order, drop exact repeats (Lever's allLocations usually repeats location).
    unique = list(dict.fromkeys(names))
    return {"name": LOCATION_SEPARATOR.join(unique)} if unique else None


def _departments(names):
    names = [n for n in (_str_or_none(x) for x in names) if n]
    return [{"name": n} for n in names] or None


def greenhouse(job: dict) -> dict:
    location = job.get("location")
    departments = job.get("departments")
    return {
        "id": str(job["id"]),
        "title": _str_or_none(job.get("title")),
        "content": _str_or_none(job.get("content")),
        "location": _location([location.get("name")]) if isinstance(location, dict) else None,
        "departments": _departments([d.get("name") for d in departments if isinstance(d, dict)])
                       if isinstance(departments, list) else None,
        "updated_at": _str_or_none(job.get("updated_at")),
        "absolute_url": _str_or_none(job.get("absolute_url")),
        "source_ats": "greenhouse",
    }


def ashby(job: dict) -> dict:
    secondary = job.get("secondaryLocations")
    secondary = secondary if isinstance(secondary, list) else []
    return {
        "id": str(job["id"]),
        "title": _str_or_none(job.get("title")),
        # HTML is what rule.py expects; the plain text is the same source, not an invention.
        "content": _str_or_none(job.get("descriptionHtml")) or _str_or_none(job.get("descriptionPlain")),
        "location": _location([job.get("location")]
                              + [s.get("location") for s in secondary if isinstance(s, dict)]),
        "departments": _departments([job.get("department")]),
        # Ashby publishes publishedAt, not an update time; it is not relabeled.
        "updated_at": None,
        "absolute_url": _str_or_none(job.get("jobUrl")),
        "source_ats": "ashby",
    }


def _lever_content(job: dict):
    parts = [_str_or_none(job.get("description")) or _str_or_none(job.get("descriptionPlain"))]
    # Lever keeps requirements in "lists"; skills and sponsorship text often live there.
    for item in job.get("lists") if isinstance(job.get("lists"), list) else []:
        if isinstance(item, dict):
            parts.append(_str_or_none(item.get("text")))
            parts.append(_str_or_none(item.get("content")))
    parts.append(_str_or_none(job.get("additional")) or _str_or_none(job.get("additionalPlain")))
    parts = [p for p in parts if p]
    return "\n".join(parts) if parts else None


def lever(job: dict) -> dict:
    categories = job.get("categories") if isinstance(job.get("categories"), dict) else {}
    all_locations = categories.get("allLocations")
    all_locations = all_locations if isinstance(all_locations, list) else []
    return {
        "id": str(job["id"]),
        "title": _str_or_none(job.get("text")),
        "content": _lever_content(job),
        "location": _location([categories.get("location")] + all_locations),
        "departments": _departments([categories.get("department")]),
        # Lever publishes createdAt, not an update time; it is not relabeled.
        "updated_at": None,
        "absolute_url": _str_or_none(job.get("hostedUrl")),
        "source_ats": "lever",
    }


NORMALIZERS = {"greenhouse": greenhouse, "ashby": ashby, "lever": lever}


def normalize(ats: str, job: dict) -> dict:
    return NORMALIZERS[ats](job)
