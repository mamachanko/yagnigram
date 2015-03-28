import textwrap

from instagram.client import InstagramAPI
from PIL import Image

from files import make_image_dir, delete_image_dir, get_media_filename, download_media
from image import UnicodeImage


def feed(count=1, width=100, token=None):
    if token is None:
        raise RunTimeError('token cannot be None')

    rendered_media_feed = []
    instagram_api = InstagramAPI(access_token=token)
    media_feed, _ = instagram_api.user_media_feed(count=count)
    make_image_dir()

    for media in media_feed:
        rendered_media = render_media(media, width=width)
        rendered_media_feed.append(rendered_media)
    return '\n'.join(rendered_media_feed)


def render_media(media, width=150):
    lines = []
    unicode_image = get_as_unicode(media, width=width)
    lines.extend(unicode_image.get_lines())
    lines.append('by %s' % media.user.username)
    lines.extend(textwrap.wrap('%s' % media.caption.text, width/2))
    if hasattr(media, 'location'):
        if media.location.name:
            lines.append('@ %s' % media.location.name)
    return '\n'.join(lines)


def get_as_unicode(media, width=150):
    media_filename = get_media_filename(media)
    try:
        image = Image.open(media_filename)
    except IOError:
        image_filename = download_media(media, media_filename)
        image = Image.open(media_filename)
    return UnicodeImage(image, width=width)

