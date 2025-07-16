def validate_image_url(url):
    is_valid = True

    if url == "":
        is_valid = False
    if url.startswith("http://") == False and url.startswith("https://") == False:
        is_valid = False
    if url.endswith(".jpg") == False and url.endswith(".jpeg") == False and url.endswith(".png") == False:
        is_valid = False

    return is_valid
