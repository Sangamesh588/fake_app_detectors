from urllib.parse import urlparse, parse_qs

def package_from_play_store_url(url: str) -> str | None:
    parsed = urlparse(url)
    if "play.google.com" not in parsed.netloc:
        return None
    qs = parse_qs(parsed.query)
    ids = qs.get("id")
    if not ids:
        return None
    return ids[0]
