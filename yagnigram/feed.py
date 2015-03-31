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

        terminal = blessings.Terminal()

        return u'{}\n{} ({})\n{} likes\n({},...)\n{} comments\n({},...)'.format(
            self.render_image(),
            terminal.bold(self.render_username()),
            self.render_created_at(),
            self.render_like_count(),
            self.render_likes(),
            self.render_comment_count(),
            self.render_comments(width),
        )

    def render_image(self, width=150):
        return UnicodeImage(self.image, width=width)

    def render_username(self, width=None):
        return self.media.user.username

    def render_created_at(self, width=None):
        return arrow.get(self.media.created_time).humanize()

    def render_like_count(self, width=None):
        return self.media.like_count

    def render_likes(self, width=150):
        return u', '.join(map(u'{0.username}'.format, self.media.likes))

    def render_comment_count(self, width=None):
        return unicode(self.media.comment_count)

    def render_comments(self, width=None):
        return u', '.join(map(u'{0.user.username}: {0.text}'.format, self.media.comments))
