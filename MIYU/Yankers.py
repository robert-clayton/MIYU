from urllib.request import urlopen
import requests
import random
import string

def _getResponse():
    # Gets a valid response
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits

    while True:
        randString = ''.join(random.choice(chars) for _ in range(5))
        url = f'http://i.imgur.com/{randString}.png'
        response = requests.get(url)
        contentType = response.headers['Content-Type']
        if len(response.content) != 503:
            if contentType == 'image/jpeg':
                response.url = url.replace('png', 'jpg')
                return response
            elif contentType == 'image/gif':
                response.url = url.replace('png', 'gif')
                return response

def randomImgurResponses(amount):
    """Yields a random image link amount times.

    :param int amount: The number of images to yield.
    """
    for _ in range(amount):
        yield _getResponse()

def randomImgurResponse():
    """Returns a single random image link."""
    return _getResponse()
