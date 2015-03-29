import textwrap

from instagram.client import InstagramAPI
from PIL import Image

from files import make_image_dir, delete_image_dir, get_media_filename, download_media
from image import UnicodeImage


class Feed(object):

    def __init__(self, token, count=1, width=100):
        self.token = token
        self.count = count
        self.width = width
        self.api = InstagramAPI(access_token=self.token)

    def load(self):
        self._feed, _ = self.api.user_media_feed(count=self.count)

    def __iter__(self):
        try:
            self._feed
        except AttributeError:
            self.load()
        for media in self._feed:
            media = Media(media)
            media.load()
            yield media.render(self.width)


class Media(object):

    def __init__(self, media):
        self.media = media

    def load(self):
        media_filename = get_media_filename(self.media)
        try:
            self.image = Image.open(media_filename)
        except IOError:
            image_filename = download_media(self.media, media_filename)
            self.image = Image.open(media_filename)

    def render(self, width=150):
        unicode_image = UnicodeImage(self.image, width=width)
        return '%s\n%s' % (unicode_image, self.media.user.username)

