"""
Usage:
    yagnigram feed [--count=<count>] [--no-images] [--use-cache] [--token=<token>] [--interactive] [--width=<width>] [--animate]
    yagnigram show <id>
    yagnigram oauth [--force] [--outputfile=<outputfile>]
    yagnigram flush_cache
    yagnigram --help
    yagnigram --version

Options:
    --help                     shows this screen
    --version                  shows version
    --count=<count>            how many media to show [default: 1]
    --width=<width>            image width [default: 100]
    --no-images                does not download and render images
    --use-cache                uses local image cache
    --token=<token>            Instagram access token
    --interactive              use interactive mode
    --animate                  animates videos
    --force                    overwrites the existing token
    --outputfile=<outputfile>  the file to write the token to [default: ~/.yagnigram]

"""
import sys
import os

from docopt import docopt

from oauth import get_oauth_token
from feed import feed


if __name__ == '__main__':
    arguments = docopt(doc=__doc__, version='Yagnigram 0.1.0')

    if arguments['oauth']:
        token_file = os.path.expanduser(arguments['--outputfile'])
        if arguments['--force']:
            try:
                os.remove(token_file)
            except OSError:
                pass
        raw_input('press any key to continue in the browser\n')
        get_oauth_token(token_file=token_file)
        print('\nYour Instagram access token has been written to  %s.' % token_file)
        print('Thank you.')

    if arguments['feed']:
        token = arguments['--token']
        width = int(arguments['--width'])
        count = int(arguments['--count'])
        print(feed(count=count, width=width, token=token))
