import os
import shutil

from instagram.client import InstagramAPI
from PIL import Image
import requests

from image import UnicodeImage


IMAGE_CACHE_DIR = './images'


def make_image_dir():
    try:
        os.mkdir(IMAGE_CACHE_DIR)
    except OSError:
        delete_image_dir()
        os.mkdir(IMAGE_CACHE_DIR)


def delete_image_dir():
    shutil.rmtree(IMAGE_CACHE_DIR)


def get_media_filename(media):
    return './images/{0}.jpg'.format(media.id)


def download_media(media, target_filename):
    media_url = media.images.get('low_resolution').url
    download_file(media_url, target_filename)


def download_file(url, target_filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(target_filename, 'wb') as image_file:
            for chunk in response.iter_content():
                image_file.write(chunk)

