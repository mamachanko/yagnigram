import abc
import tempfile
import textwrap

from instagram.client import InstagramAPI
from PIL import Image
import requests
import six

from image import UnicodeImage


class Feed(object):

    def __init__(self, token, count=10):
        self.token = token
        self.count = count

    def __iter__(self):
        self.load()
        for content in self.contents:
            yield FeedItem(content)

    def load(self):
        instagram_api = InstagramAPI(access_token=self.token)
        self.contents, _ = instagram_api.user_media_feed(count=self.count)


class FeedItem(object):

    def __init__(self, media):
        self.media = media

    def load(self):
        response = requests.get(self.url, stream=True)
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile('w+b') as f:
                for chunk in response.iter_content():
                    f.write(chunk)
                self.image = Image.open(f.name)
        else:
            raise RunTimeError('could not load {}. http status: {}'.format(self.url, response.status_code))

    @property
    def url(self):
        return self.media.images.get('low_resolution').url

    def render(self, width=150):
        try:
            self.load()
        except RunTimeError as error:
            return error.msg

        unicode_image = UnicodeImage(self.image, width=width)
        return '{}\n{}'.format(unicode_image, self.media.user.username)
