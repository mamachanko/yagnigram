"""
Usage:
    yagnigram feed [--count=<count>] [--no-images] [--use-cache] [--token=<token>] [--tokenfile=<tokenfile>] [--interactive] [--width=<width>] [--animate]
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
    --tokenfile=<tokenfile>    file containing the Instagram access token [default: ~/.yagnigram]
    --interactive              use interactive mode
    --animate                  animates videos
    --force                    overwrites the existing token
    --outputfile=<outputfile>  the file to write the token to [default: ~/.yagnigram]

"""
import sys
import os

from docopt import docopt

from oauth import handle_oauth
from feed import Feed


if __name__ == '__main__':
    arguments = docopt(doc=__doc__, version='Yagnigram 0.1.0')

    if arguments['oauth']:
        output_file = os.path.expanduser(arguments['--outputfile'])
        if arguments['--force']:
            try:
                os.remove(output_file)
            except OSError:
                pass
        raw_input('press any key to continue in the browser\n')
        handle_oauth(output_file=output_file)
        print('\nYour Instagram access token has been written to  %s.' % output_file)
        print('Thank you.')

    if arguments['feed']:
        if arguments['--token']:
            token = arguments['--token']
        else:
            token_file = os.path.expanduser(arguments['--tokenfile'])
            with open(token_file, 'r') as f:
                token = f.readline()
        width = int(arguments['--width'])
        count = int(arguments['--count'])
        for media in Feed(token, count=count, width=width):
            print(media)
