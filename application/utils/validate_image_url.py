def validate_image_url(url):
    if url == "":
        return True
    if url.startswith("http://") or url.startswith("https://"):
        return True
    if url.endswith(".jpg") or url.endswith(".jpeg") or url.endswith(".png"):
        return True
    return False
