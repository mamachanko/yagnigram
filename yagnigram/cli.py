import sys
import os

import blessings
import click

from yagnigram import oauth, feed

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
@click.option('--width', default=100, help='The width of images and text')
@click.option('--count', default=1, help='The number of posts to show')
def _feed(width, count):
    try:
        token = get_token()
    except IOError:
        click.echo('Could not read token from {}. Try `yagnigram login` first.'.format(TOKENFILE))
        return

    for feed_item in feed.Feed(token, count=count):
        print(feed_item.render(width))

 
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

