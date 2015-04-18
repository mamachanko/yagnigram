import abc
import tempfile
import textwrap

import arrow
import blessings
from instagram.client import InstagramAPI
from PIL import Image
import requests
import six

from image import UnicodeImage


class Feed(object):

    def __init__(self, token):
        self.token = token

    def __iter__(self):
        instagram_api = InstagramAPI(access_token=self.token)
        for content, _ in instagram_api.user_media_feed(count=1, as_generator=True, max_pages=None):
            media = Media(content[0])
            media.load()
            yield FeedItem(media)


class FeedItem(object):

    def __init__(self, media):
        self.media = media
        
    def get_image(self, width=150):
        return u'{}'.format(UnicodeImage(self.media.image, width=width))

    def get_meta(self, width=150):
        meta = [
            self.media.username,
            self.media.created_time,
        ]

        if self.media.like_count:
            meta.extend([
                '{} likes'.format(self.media.like_count),
                '{}'.format(self.media.likes)
            ])
        else:
            meta.append('no likes yet')

        if self.media.comment_count:
            meta.extend([
                '{} comments'.format(self.media.comment_count),
                '{}'.format(self.media.comments)
            ])
        else:
            meta.append('no comments yet')

        return u'\n'.join(meta)


class Media(object):

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
            error_message = "couldn't load {}. http status: {}".format(
                self.url, response.status_code
            )
            raise RunTimeError(error_message)

    @property
    def url(self):
        return self.media.images.get('low_resolution').url

    #def image(self, width=150):
    #    return UnicodeImage(self.image, width=width)

    @property
    def username(self):
        return self.media.user.username

    @property
    def created_time(self):
        return arrow.get(self.media.created_time).humanize()

    @property
    def like_count(self):
        return self.media.like_count

    @property
    def likes(self):
        return map(u'{0.username}'.format, self.media.likes)

    @property
    def comment_count(self, width=None):
        return self.media.comment_count

    @property
    def comments(self):
        return map(u'{0.user.username}: {0.text}'.format, self.media.comments)
