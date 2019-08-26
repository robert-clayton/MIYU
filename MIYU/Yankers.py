from urllib.request import urlopen
import random
import string

def _getUrl():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits

    while True:
        randString = ''.join(random.choice(chars) for _ in range(5))
        url = f'http://i.imgur.com/{randString}.png'
        response = urlopen(url)
        metadata = response.info()
        contentLength = int(metadata['Content-Length'])
        contentType = metadata['Content-Type']

        # If not error, increment counter and yield url fixed to type
        if contentLength != 503:
            if contentType == 'image/jpeg':
                return url.replace('png', 'jpg')
            elif contentType == 'image/gif':
                return url.replace('png', 'gif')

def randomImages(amount):
    """Yields a random image link amount times.

    :param int amount: The number of images to yield.
    """
    for _ in range(amount):
        yield _getUrl()

def randomImage():
    """Returns a single random image link."""
    return _getUrl()
