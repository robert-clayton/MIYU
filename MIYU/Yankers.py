import urllib
from urllib.request import urlopen
import random
import string

def randomImage(amount):
    """Yields a random image for amount times.

    :param int amount: The number of images to yield.
    """
    successful = 0
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    # Keep the generator going until the desired amount of successful iterations
    while successful < amount:
        randString = ''.join(random.choice(chars) for _ in range(5))
        url = f'http://i.imgur.com/{randString}.png'
        response = urlopen(url)
        metadata = response.info()
        contentLength = int(metadata['Content-Length'])
        contentType = metadata['Content-Type']

        # If not error, increment counter and yield url fixed to type
        if contentLength != 503:
            successful += 1
            if contentType == 'image/jpeg':
                yield url.replace('png', 'jpg')
            elif contentType == 'image/gif':
                yield url.replace('png', 'gif')

if __name__ == '__main__':
    import time
    t0 = time.time()
    print(list(randomImage(1000)))
    print(time.time() - t0)
        