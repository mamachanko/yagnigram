import sys
import os

import blessings
import click

from yagnigram import oauth, feed, image
from yagnigram.image import UnicodeImage

TOKENFILE = os.path.expanduser('~/.yagnigram')


@click.group()
def cli():
    pass


@cli.command()
def login():
    click.echo('Welcome to ' + click.style('yagnigram', bold=True))
    remove_tokenfile()
    raw_input('press any key to continue in the browser\n')
    oauth.handle_oauth(outputfile=TOKENFILE)
    print('\nYour Instagram access token has been written to %s' % TOKENFILE)
    print('Thank you.')


@cli.command()
def logout():
    remove_tokenfile()
    click.echo('You have logged out of ' + click.style('yagnigram', bold=True))


@cli.command('feed')
def _feed():
    try:
        token = get_token()
    except IOError:
        click.echo('Could not read token from {}. Try `yagnigram login` first.'.format(TOKENFILE))
        return

    terminal = blessings.Terminal()
    for feed_item in feed.Feed(token):
        with terminal.fullscreen():
            print(feed_item.get_image(width=terminal.width))
            print(feed_item.get_meta(width=terminal.width))
            raw_input()


@cli.command()
def test():
    """
    Shows a test image which should use terminal dimensions optimally.
    The image is supposed to be square.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    sample_image = os.path.join(root_dir, 'tests/sample.jpg') 
    terminal = blessings.Terminal()
    width, height = terminal.width, int(terminal.width*.8)
    unicode_image = UnicodeImage.from_filename(
        sample_image, width=width, height=height
    )
    with terminal.fullscreen():
        click.echo(u'{}'.format(unicode_image))
        raw_input('{t.width} x {t.height}'.format(t=terminal))


def remove_tokenfile():
    try:
        os.remove(TOKENFILE)
    except OSError:
        pass


def get_token():
    try:
        with open(TOKENFILE, 'r') as f:
            return f.readline()
    except IOError:
        raise

